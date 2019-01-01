var log = console.log.bind(console)

var e = function(selector, parent=document) {
    return parent.querySelector(selector)
}


var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            log('load ajax response', r.response)
            var json = JSON.parse(r.response)
            responseCallback(json)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}
