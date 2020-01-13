API = {
        '/cookies_this_site': {
            'GET': {
                'params': {
                    'site': '站点'
                },
                'return': {"total": '站点总数', "sites":  '["siteA", "siteB"]'},
                'coment': '获取所有的站点'
            },
            "POST": {
                'body': {
                    'site': '站点',
                    'check_key': '要校验的关键字',
                    'headers': 'headers必须是严格json',
                    'method': 'get/post请求方式',
                },
                'return': '{"code": 0, "msg": "ok!"}',
                'coment': '新建/修改一个站点信息'
            }
        },
        '/cookeis': {
            'GET': {
                'params': {
                    'site': 'site',
                    'strategy': 'random/order 随机取出一条可用的cookies, 内部会维护一个取出顺序, 使用order时候会循环顺序取出一个',
                },
                'return': '{cookies: {cookies: "xxx", cookies_name: "xxx", created: "2020-01-13 05:24:07", id: 3,…}}',
                'coment': '获取一条可用的cookies记录'
            },
            'POST': {
                'body': {
                    'site': 'site',
                    'cookies': '要添加的的cookies',
                    'cookies_name': '要添加的cookies_name(可以不传)',

                },
                'return': '{"code": 0, "msg": "ok!"}',
                'coment': '添加一条新的cookies记录'
            },
            'PUT': {
                'body': {
                    'cookies_id': 'cookies_id',
                    'cookies': '要修改的cookies',           
                    'cookies_name': '要修改的cookies_name',

                },
                'return': '{"code": 0, "msg": "ok!"}',
                'coment': '根据cookies_id修改对应的cookies值'
            },
            'DELETE': {
                'params': {
                    'cookies_id': 'cookies_id',

                },
                'return': '{"code": 0, "msg": "ok!"}',
                'coment': '根据cookies_id删除对应的记录'
            }
        }
    }