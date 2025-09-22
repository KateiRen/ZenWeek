// dragdrop.js - Handles all drag-and-drop and task interaction logic for ZenWeek

$(document).ready(function() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    var dragging = null;
    function getTarget(target) {
        while (target.nodeName.toLowerCase() != 'li' && target.nodeName.toLowerCase() != 'body' && target.nodeName.toLowerCase() != 'button' && target.nodeName.toLowerCase() != 'a') {
            target = target.parentNode;
        }
        if (target.nodeName.toLowerCase() == 'body') {
            return false;
        } else {
            return target;
        }
    }

    document.addEventListener('dragstart', function(event) {
        var target = getTarget(event.target);
        dragging = target;
        event.dataTransfer.setData('text/plain', null);
        // Only set drag image if dragging is a valid Element
        if (dragging instanceof Element) {
            event.dataTransfer.setDragImage(dragging, 0, 0);
        }
    });

    document.addEventListener('dragover', function(event) {
        event.preventDefault();
        var target = getTarget(event.target);
        if (target==false) {
            //
        } else if (target.matches("li")) {
            var bounding = target.getBoundingClientRect()
            var offset = bounding.y + (bounding.height/2);
            if ( event.clientY - offset > 0 ) {
                target.style['border-bottom'] = 'solid 4px blue';
                target.style['border-top'] = '';
            } else {
                target.style['border-top'] = 'solid 4px blue';
                target.style['border-bottom'] = '';
            }
        } else if (target.matches("button")) {
            target.style['border'] = 'solid 4px blue';
        }
    });

    document.addEventListener('dragleave', function(event) {
        var target = getTarget(event.target);
        if (target) {
            target.style['border'] = '';
        }
    });

    document.addEventListener('drop', function(event) {
        event.preventDefault();
        var target = getTarget(event.target);
        if (target!=false) {
            if (target.matches("button")) {
                if (target.matches("#editbutton")) {
                    target.style['border'] = '';
                    document.getElementById("taskEditModal-taskid").value = $(dragging).attr("taskid");
                    document.getElementById("taskEditModal-year").value = $(dragging).parent().attr("year");
                    document.getElementById("taskEditModal-week").value = $(dragging).parent().attr("week");
                    document.getElementById("taskEditModal-task").value = $(dragging).children("span").text();
                    if ($(dragging).children("a").length) {
                        document.getElementById("taskEditModal-taskurl").value = $(dragging).children("a").attr("href");
                    } else {
                        document.getElementById("taskEditModal-taskurl").value = "";
                    }
                    $("#taskEditModal").modal("show", {backdrop: true, keyboard: true});
                } else if (target.matches("#deletebutton")) {
                    target.style['border'] = '';
                    url = "deleteTask" + "?taskid=" + $(dragging).attr("taskid")
                    $.ajax({
                        url: url,
                        type: "get",
                        success: function(data){
                            $(dragging).remove()
                        }, 
                        error: function(xhr){
                        }
                    });
                }
            } else if (target.matches(".cw-button")) {
                if (!target.matches(".cw-button-selected")) {
                    url = "moveTask" + $(target).attr("href") + "&taskid=" + $(dragging).attr("taskid")
                    $.ajax({
                        url: url,
                        type: "get",
                        success: function(data){
                            $(dragging).remove()
                        }, 
                        error: function(xhr){
                        }
                    });
                }
            } else if (target.matches("li")) {
                if ( target.style['border-bottom'] !== '' ) {
                    target.style['border-bottom'] = '';
                    target.parentNode.insertBefore(dragging, event.target.nextSibling);
                } else {
                    target.style['border-top'] = '';
                    target.parentNode.insertBefore(dragging, event.target);
                }
                counter = 1;
                $(target).parent().children().each( function () {
                    child = $(this);
                    if(child.attr("taskid")) {
                        if(child.parent().hasClass("dailytasks")) {
                            url = "updateTask?taskid=" + child.attr("taskid") + "&date=" + child.parent().attr("date") + "&order=" + counter;
                        } else {
                            url = "updateTask?taskid=" + child.attr("taskid") + "&order=" + counter;
                        }
                        $.get(url,function(d){});
                        counter += 1;
                    }
                });
            }
        }
    });

    // submit on ENTER
    $(".createTask").each(function() {
        $(this).keypress(function(event) {
            if (event.keyCode == 13 || event.which == 13) {
                $(this).parent().parent().submit();
                event.preventDefault();
            }
        })
    });

    // submit on Click auf den Pfeil
    $(".createTask2").each(function() {
        $(this).click(function(event) {
            $(this).parent().parent().submit();
            event.preventDefault();
        })
    });

    function editTask(taskid, action){
        url = '/editTask?taskid=' + taskid + '&action=' + action;
        $.ajax({
            url: url,
            type: "get",
            success: function(response) {},
            error: function(xhr) {}
        });
    };

    $('body').on('click', '.task-toggle', function() {
        taskid = $(this).parent().attr("taskid")
        if ($(this).siblings("span").hasClass("task-done")) {
            $(this).siblings("span").removeClass("task-done")
            $(this).removeClass("bi-check-square")
            $(this).addClass("bi-square")
            editTask(taskid,"undo");
        } else {
            $(this).siblings("span").addClass("task-done")
            $(this).removeClass("bi-square")
            $(this).addClass("bi-check-square")
            editTask(taskid,"done");
        }
    });

    $.fn.loadWith2 = function(){
        var c=$(this);
        url = c.attr("url")
        $.get(url,function(d){c.html(d);});
    };

    $(".weeklytasks").loadWith2();
    $(".dailytasks").each(function(index, element) {
        $(this).loadWith2()
    });
});
