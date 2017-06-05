import requests
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from lockdown.decorators import lockdown

from twilio.rest import Client

from screener.models import ScreenModel, ResourceModel

FORM_PARAMS = ['zip_code', 'insurance_uid', 'specialty_uid', 'gender']


def parse_params(param_dict):
    params = {}
    for p in FORM_PARAMS:
        if param_dict.get(p):
            params[p] = param_dict.get(p)
    return params


def get_best_practices(practices):
    best_practices = list(filter(
        lambda p: p['within_search_area'] and len(p.get('phones', [])) > 0 and p['accepts_new_patients'],
        practices
    ))
    return sorted(best_practices, key=lambda p: p['distance'])


def query_providers(params, skip=0):
    params = params.copy()
    params['skip'] = skip
    params['user_key'] = settings.BETTER_DOCTOR_API_KEY
    params['sort'] = 'distance-asc'
    zip_code = params.pop('zip_code')
    coords = settings.ZIP_MAP.get(str(zip_code), (41.837, -87.685))
    params['location'] = '{},{},30'.format(*coords)
    params['limit'] = settings.PAGE_COUNT
    r = requests.get(settings.BETTER_DOCTOR_URL, params=params)

    doc_dicts = []
    for doc in r.json()['data']:
        practices = get_best_practices(doc['practices'])
        if not len(practices):
            continue
        practice = practices[0]
        d = {}
        d['full_name'] = doc['profile']['first_name'] + ' ' + doc['profile']['last_name']
        loc = practice['visit_address']
        street = loc['street']
        if 'street2' in loc:
            street += ' ' + loc['street2']
        d['location'] = '{} \n{}, {} {}'.format(
            street, loc['city'], loc['state'], loc['zip']
        )
        phone = practice['phones'][0]['number']
        d['phone'] = '{}-{}-{}'.format(phone[:3], phone[3:6], phone[6:])
        d['npi'] = doc['npi']
        doc_dicts.append(d)

    return doc_dicts


# TODO: Pull insurance and specialty options
def get_api_options():
    return {
        'gender_options': [
            {'value': 'female', 'display': 'Female'},
            {'value': 'male', 'display': 'Male'}
        ],
        'specialty_options': [
            {'value': 'family-practitioner,family-nurse-practitioner,general-practitioner,nurse-practitioner,family-medicine-adult-medicine',
            'display': 'Family Medicine'},
            {'value': 'endocrinologist', 'display': 'Endocrinologist'},
            {'value': 'foot-ankle-orthopedist', 'display': 'Foot and Ankle Surgeon'}
        ],
        'insurance_options': [
            {'value': 'medicaid-medicaid', 'display': 'Medicaid'},
            {'value': 'aetna-aetnadmo', 'display': 'Aetna DMO'},
            {'value': 'aetna-aetnadmo', 'display': 'Aetna HMO'}
        ]
    }


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, get_api_options())

    # Submits params to APIs, creates Screen objects with those params, redirects
    def post(self, request, *args, **kwargs):
        post_args = request.POST.dict()
        params = parse_params(post_args)
        if len(params.keys()) == 0:
            return render(
                request,
                self.template_name,
                {'message': 'Must include search terms for providers'}
            )
        screen_obj = ScreenModel(
            ScreenModel.make_slug(),
            created_at=datetime.now(),
            params=params,
            phone=post_args.get('phone'),
            email=post_args.get('email'),
            visits=-1
        )
        screen_obj.save()

        return HttpResponseRedirect(
            reverse('screen',
            kwargs={'slug': screen_obj.slug})
        )


class ScreenView(TemplateView):
    template_name = 'screener.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ScreenView, self).dispatch(request, *args, **kwargs)

    # Renders template based on pre-created slug
    def get(self, request, *args, **kwargs):
        try:
            screen_obj = ScreenModel.get(kwargs['slug'])
        except ScreenModel.DoesNotExist:
            return HttpResponseBadRequest()

        skip_val = int(request.GET.get('skip', 0))
        # Only update visits count if it's the first page
        if skip_val == 0:
            screen_obj.update({
                'visits': {
                    'action': 'add',
                    'value': 1
                }
            })

        provider_info = query_providers(
            screen_obj.params, skip=skip_val
        )
        response_dict = {'screen': screen_obj, 'providers': provider_info}
        if skip_val >= settings.PAGE_COUNT:
            response_dict['prev_skip'] = skip_val - settings.PAGE_COUNT
        if len(provider_info) == settings.PAGE_COUNT:
            response_dict['next_skip'] = skip_val + settings.PAGE_COUNT

        response_dict.update(get_api_options())
        return render(request, self.template_name, response_dict)

    def post(self, request, *args, **kwargs):
        post_args = request.POST.dict()
        params = parse_params(post_args)
        if len(params.keys()) == 0:
            return JsonResponse({'message': 'Must include search terms for providers'})
        try:
            screen_obj = ScreenModel.get(kwargs['slug'])
        except ScreenModel.DoesNotExist:
            return JsonResponse({'message': 'Not found'})

        screen_obj.update({
            'params': {
                'action': 'put',
                'value': params
            },
            'phone': {
                'action': 'put',
                'value': post_args.get('phone')
            },
            'email': {
                'action': 'put',
                'value': post_args.get('email')
            }
        })

        provider_info = query_providers(params)
        response_dict = {'screen': screen_obj, 'providers': provider_info}
        response_dict['next_skip'] = settings.PAGE_COUNT

        response_dict.update(get_api_options())
        if request.GET.get('format') == 'json':
            return JsonResponse(provider_info)
        return render(request, self.template_name, response_dict)


class SendTextView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(SendTextView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            screen_obj = ScreenModel.get(kwargs['slug'])
        except ScreenModel.DoesNotExist:
            return HttpResponseBadRequest()

        patient_number = screen_obj.phone
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        provider_info = query_providers(screen_obj.params)
        msg_docs = []
        for doc in provider_info:
            msg_docs.append('Name: {}\nPhone: {}\nOffice: {}\n\n'.format(
                doc['full_name'], doc['phone'], doc['location'])
            )

        client.messages.create(
            to=patient_number,
            from_=settings.TWILIO_CALLER_ID,
            body= ''.join(msg_docs) + 'https://' + request.get_host() + reverse('screen', kwargs=kwargs)
        )
        return HttpResponseRedirect(reverse('screen', kwargs=kwargs))


class ProviderDetailView(TemplateView):
    template_name = 'detail.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ProviderDetailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response_dict = {'npi': kwargs['npi']}
        return render(request, self.template_name, response_dict)


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(lockdown())
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        screens = ScreenModel.scan()
        param_list = [
            dict(
                params=s.params,
                date=s.created_at.strftime('%Y-%m-%d'),
                visits=s.visits
            ) for s in screens
        ]
        return render(request, self.template_name, {'param_list': param_list})
