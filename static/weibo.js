
var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
//    r = ajax('GET', path, '', callback)
//    callback(r)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weibo_id, callback) {
    var path = `/api/weibo/delete?id=${weibo_id}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiWeiboComment = function(form, callback) {
    var path = '/api/weibo/comment'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(comment_id, callback) {
    var path = `/api/weibo/comment/delete?id=${comment_id}`
    ajax('GET', path, '', callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = '/api/weibo/comment/update'
    ajax('POST', path, form, callback)
}

// var apiUser = function(callback) {
//     var path = `/api/weibo/owner`
//     ajax('GET', path, '', callback)
// }

var weiboTemplate = function(weibo) {
    let comment = weibo.comment || []
    let commentList = ''
    for (let i=0; i<comment.length; i++) {
        let c =  `
        <div class="comment-cell" data-id="${comment[i].id}">
            <p style="border:1px red solid">
            <span class="weibo-comment-span">${comment[i].username}评论：${comment[i].content}</span>
            <button class="comment-delete">删除</button>
            <button class="comment-edit">编辑</button>
            </p>
        </div>
        `
        commentList += c
    }
    let t = `
        <div class="weibo-cell" data-id="${weibo.id}">
            <br>
            <span class="weibo-content">${weibo.username}：${weibo.content}</span>
            <button class="weibo-edit">编辑</button>
            <button class="weibo-delete">删除</button>
            <br>
            <input class="weibo-comment-input">
            <button class="weibo-comment">添加评论</button>
            <br>
            ${commentList}
        </div>
    `
    return t
}

var weiboUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-content" value="${content}">
            <button class="weibo-update">更新</button>
        </div>
    `
    return t
}

var weiboCommentTemplate = function(comment) {
// <span class="todo-id" hidden=True>${todo.id}</span>
    var t = `
        <div class="comment-cell" data-id="${comment.id}">
            <p style="border:1px red solid">
            <span class="weibo-comment-span">${comment.username}评论：${comment.content}</span>
            <button class="comment-delete">删除</button>
            <button class="comment-edit">编辑</button>
            </p>
        </div>
    `
    return t
}

var commmentUpdateTemplate = function(content) {
    var t = `
        <div class="comment-update-form">
            <input class="comment-update-content" value="${content}">
            <button class="comment-update">更新</button>
        </div>
    `
    return t
}

var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var insertUpdateForm = function(content, weiboCell) {
    var weiboUpdateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('afterend', weiboUpdateForm)
}

var insertComment = function(comment, weiboCell) {
    var commentTemplate = weiboCommentTemplate(comment)
    // var commentSpace = e('.weibo-cell', weiboCell)
    weiboCell.insertAdjacentHTML('beforeend', commentTemplate)
}

var insertCommentUpdateForm = function(content, commentCell) {
    var commentUpdateForm = commmentUpdateTemplate(content)
    commentCell.insertAdjacentHTML('beforeend', commentUpdateForm)
}

var loadWeibos = function() {
    apiWeiboAll(function(forms) {
        log('load all weibos', forms)
        for(var i = 0; i < forms.length; i++) {
            var weibo = forms[i]
            var comments = weibo['comment']
            insertWeibo(weibo)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    log('click!', b)
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(weibo) {
            insertWeibo(weibo)
        })
    })
}

var bindEventWeiboDelete = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('weibo-delete')) {
        log('点到了删除按钮')
        var weiboId = self.parentElement.dataset['id']
        apiWeiboDelete(weiboId, function(r) {
            log('apiWeiboDelete', r.message)
            alert(r.message)
            if (r.message.indexOf("成功删除 weibo") != -1) {
                self.parentElement.remove()
            } else {
                log('没有权限')
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('weibo-edit')) {
        log('点到了编辑按钮')
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var weiboSpan = e('.weibo-content', weiboCell)
        var insertSpan = e('.weibo-comment', weiboCell)
        var content = weiboSpan.innerText
        log('weibo edit', weiboId, content)
        insertUpdateForm(content, insertSpan)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('weibo-update')) {
        log('点到了更新按钮')
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var weiboInput = e('.weibo-update-content', weiboCell)
        var content = weiboInput.value
        log('weibo update', weiboId, content)
        var form = {
            id: weiboId,
            content: content,
        }
        apiWeiboUpdate(form, function(weibo) {
            log('apiWeiboUpdate', weibo)
            if (weibo.hasOwnProperty('message')) {
                log('没有权限')
                bindEventUser()
            } else {
                log('apiWeiboUpdate更新成功')
                var weiboSpan = e('.weibo-content', weiboCell)
                weiboSpan.innerText = weibo.content

                var updateForm = e('.weibo-update-form', weiboCell)
                updateForm.remove()
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboComment = function () {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
        var self = event.target
        if (self.classList.contains('weibo-comment')) {
            var weiboCell = self.closest('.weibo-cell')
            var commentCell = self.closest('.comment-cell')
            var weiboId = weiboCell.dataset['id']
            var commentInput = e('.weibo-comment-input', weiboCell)
            var comment = commentInput.value
            var form = {
                // id: weiboId
                content: comment,
                weibo_id: weiboId,
            }
            apiWeiboComment(form, function(comment) {
                insertComment(comment, weiboCell)
            })
        } else {
            log('点到了 weibo cell')
        }
    })
}

var bindEventCommentDelete = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-delete')) {
        log('点到了删除按钮')
        var commentId = self.parentElement.parentElement.dataset['id']
        log('parentElement id', self.parentElement, commentId)
        apiCommentDelete(commentId, function(r) {
            log('apiCommentDelete', r.message)
            alert(r.message)
            if (r.message.indexOf("成功删除 comment") != -1) {
                self.parentElement.remove()
            } else {
                log('权限不足')
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-edit')) {
        log('点到了编辑按钮')
        var commentCell = self.closest('.comment-cell')
        log('commentCell', commentCell)
        var commentId = commentCell.dataset['id']
        var commentSpan = e('.weibo-comment-span', commentCell)
        var content = commentSpan.innerText
        log('comment edit', commentId, content)
        insertCommentUpdateForm(content, commentCell)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    log(event)
    var self = event.target
    log('被点击的元素', self)
    log(self.classList)
    if (self.classList.contains('comment-update')) {
        log('点到了更新按钮')
        var commentCell = self.closest('.comment-cell')
        var commentId = commentCell.dataset['id']
        var commentInput = e('.comment-update-content', commentCell)
        var content = commentInput.value
        log('weibo update', commentId, content)
        var form = {
            id: commentId,
            content: content,
        }
        apiCommentUpdate(form, function(comment) {
            // if (comment.ContainsKey('message') = -1) {
            log('233comment', comment)
            if (comment.hasOwnProperty('message')) {
                log('没有权限')
                bindEventUser()
            } else {
              log('apiCommentUpdate', comment)

              var commentSpan = e('.weibo-comment-span', commentCell)
              commentSpan.innerText = comment.content

              var updateForm = e('.comment-update-form', commentCell)
              updateForm.remove()
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventUser = function() {
    // apiUser(function(r) {
    //     log('apiWeiboDelete', r.message)
    //     alert(r.message)
    // })
    alert('没有权限')
}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventWeiboComment()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
    // bindEventUser()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
