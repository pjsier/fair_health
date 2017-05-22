SCREEN_TABLE_DATA = {
    "Table": {
        "AttributeDefinitions": [
            {
                "AttributeName": "created_at",
                "AttributeType": "S"
            },
            {
                "AttributeName": "params",
                "AttributeType": "S"
            },
            {
                "AttributeName": "phone",
                "AttributeType": "S"
            },
            {
                "AttributeName": "email",
                "AttributeType": "S"
            },
            {
                "AttributeName": "event",
                "AttributeType": "S"
            },
            {
                "AttributeName": "visits",
                "AttributeType": "N"
            }
        ],
        "CreationDateTime": 1.363729002358E9,
        "ItemCount": 42,
        "KeySchema": [
            {
                "AttributeName": "slug",
                "KeyType": "HASH"
            }
        ],
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        },
        "TableName": "test-table",
        "TableSizeBytes": 0,
        "TableStatus": "ACTIVE"
    }
}
