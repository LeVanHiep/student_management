from model import Student

data = [
    {
        "username" : "ha",
        "password" : "12345678",
        "name" : "Lê Văn Hảo",
        "gender" : "nam",
        "grade" : "DHKTPM01",
        "school_year" : 13,
        "age" : 22,
        "permanent_address":
        {
            "unit" : "12/1A",
            "street" : "Đình Thôn",
            "ward": "Mỹ Đình",
            "district" : "Nam Từ Liêm",
            "city" : "Hà Nội",
            "country" : "Việt Nam"
        },
        "birth_address" :
        {
            "unit" : "123/1A",
            "street" : "Đình Thôn",
            "ward": "Mỹ Đình",
            "district" : "Nam Từ Liêm",
            "city" : "Hà Nội",
            "country" : "Thanh Hóa"
        },
        "prize" :
        [
            "Giải nhất cuộc thi AI Tank - IT Festival",
            "Giải nhất cuộc thi ABC"
        ]
    },
    
    {
        "username" : "hong",
        "password" : "12345678",
        "name" : "Lê Văn Hồng",
        "gender" : "nữ",
        "grade" : "DHKTPM02",
        "school_year" : 14,
        "age" : 21,
        "permanent_address":
        {
            "unit" : "124A",
            "street" : "abc",
            "ward": "abc",
            "district" : "Bắc Từ Liêm",
            "city" : "Hà Hà",
            "country" : "Hà Nội"
        },
        "birth_address" :
        {
            "unit" : "12",
            "street" : "Đình",
            "ward": "Đình",
            "district" : "Liêm",
            "city" : "Nội",
            "country" : "Trung Quốc"
        },
        "prize" :
        [
            "Giải nhất cuộc thi 1",
            "Giải nhất cuộc thi 2",
            "Giải nhất cuộc thi 3"
        ]
    },
    
    {
        "username" : "hoang",
        "password" : "12345678",
        "name" : "Lê Hoàng",
        "gender" : "nam",
        "grade" : "DHKTPM01",
        "school_year" : 1,
        "age" : 32,
        "permanent_address":
        {
            "unit" : "2A",
            "street" : "Đình",
            "ward": "Mỹh",
            "district" : "Nam Từ",
            "city" : "Hà Nội",
            "country" : "Việt Nam"
        },
        "birth_address" :
        {
            "unit" : "1231A",
            "street" : "Đôn",
            "ward": "Mình",
            "district" : "Niêm",
            "city" : "Bắc Ninh",
            "country" : "Hà Nội"
        },
        "prize" :
        [
            "Giải nhất cuộc thi 1",
            "Giải nhất cuộc thi 2",
            "Giải nhất cuộc thi 3"
        ]
    },
    
    {
        "username" : "hung",
        "password" : "12345678",
        "name" : "Lê Văn Hùng",
        "gender" : "nam",
        "grade" : "DHKTPM01",
        "school_year" : 13,
        "age" : 22,
        "permanent_address":
        {
            "unit" : "19A",
            "street" : "Đình Thôn",
            "ward": "Mỹ Đình",
            "district" : "Nam Từ Liêm",
            "city" : "Hà Nội",
            "country" : "Việt Nam"
        },
        "birth_address" :
        {
            "unit" : "23A",
            "street" : "Bưởi",
            "ward": "Táo",
            "district" : "Cam",
            "city" : "Thành phố Hồ Chí Minh",
            "country" : "Việt Nam"
        },
        "prize" :
        [
            "Giải nhất cuộc thi 1",
            "Giải nhất cuộc thi 2",
            "Giải nhất cuộc thi 3"
        ]
    },

    {
        "username" : "hao",
        "password" : "12345678",
        "name" : "Lê Hảo",
        "gender" : "nam",
        "grade" : "DHKTPM03",
        "school_year" : 11,
        "age" : 20,
        "permanent_address":
        {
            "unit" : "5",
            "street" : "Phú Mỹ",
            "ward": "Mỹ Đình",
            "district" : "Nam Từ Liêm",
            "city" : "Hà Nội",
            "country" : "Việt Nam"
        },
        "birth_address" :
        {
            "unit" : "123",
            "street" : "Soket",
            "ward": "Handsome",
            "district" : "Great K",
            "city" : "New York",
            "country" : "Mỹ"
        },
        "prize" :
        [
            "Giải nhất cuộc thi X"
        ]
    }
]
for student in data:
    print(Student.Create(student))