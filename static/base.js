var log = console.log.bind(console)

var e = function(selector, parent=document) {
    return parent.querySelector(selector)
}


var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            log('load ajax response', r.response)
            var json = JSON.parse(r.response)
            responseCallback(json)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}
