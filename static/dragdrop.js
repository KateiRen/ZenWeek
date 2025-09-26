// dragdrop.js - Handles all drag-and-drop and task interaction logic for ZenWeek

$(document).ready(function() {
    // Toggle work week / full week
    function setWeekView(mode) {
        if (mode === 'work') {
            $(".day-col").each(function() {
                var day = $(this).attr('data-day');
                if (day === 'Samstag' || day === 'Sonntag') {
                    $(this).hide();
                } else {
                    $(this).show();
                }
            });
            $('#toggle-week-switch').prop('checked', true);
            $('#toggle-week-label').text('Mo-Fr');
        } else {
            $(".day-col").show();
            $('#toggle-week-switch').prop('checked', false);
            $('#toggle-week-label').text('Mo-So');
        }
        setTimeout(setCardHeights, 200);
    }
    var weekMode = localStorage.getItem('zenweek_week_mode') || 'full';
    setWeekView(weekMode);
    $('#toggle-week-switch').on('change', function() {
        weekMode = this.checked ? 'work' : 'full';
        localStorage.setItem('zenweek_week_mode', weekMode);
        setWeekView(weekMode);
    });

    // Badge toggle logic
    function setBadgeVisibility(show) {
        if (show) {
            $('.open-task-badge').show();
        } else {
            $('.open-task-badge').hide();
        }
    }
    var badgeMode = localStorage.getItem('zenweek_badge_mode');
    if (badgeMode === null) badgeMode = 'on';
    $('#toggle-badge-switch').prop('checked', badgeMode === 'on');
    setBadgeVisibility(badgeMode === 'on');
    $('#toggle-badge-switch').on('change', function() {
        badgeMode = this.checked ? 'on' : 'off';
        localStorage.setItem('zenweek_badge_mode', badgeMode);
        setBadgeVisibility(badgeMode === 'on');
    });
    // Dynamic card height adjustment: set all cards in a visual row to the tallest card in that row
    function setCardHeights() {
        // Reset all card heights first
        var $cards = $('.container-fluid .card');
        $cards.css('height', '');
        // Group cards by their top offset (visual row)
        var rows = {};
        $cards.each(function() {
            var top = $(this).offset().top;
            // Use a tolerance to group cards in the same row (in case of subpixel differences)
            var found = false;
            for (var key in rows) {
                if (Math.abs(key - top) < 5) { // 5px tolerance
                    rows[key].push(this);
                    found = true;
                    break;
                }
            }
            if (!found) {
                rows[top] = [this];
            }
        });
        // Set height for each row
        for (var key in rows) {
            var maxHeight = 0;
            rows[key].forEach(function(card) {
                var h = $(card).outerHeight();
                if (h > maxHeight) maxHeight = h;
            });
            rows[key].forEach(function(card) {
                $(card).css('height', maxHeight + 'px');
            });
        }
    }
    setTimeout(setCardHeights, 400);
    $(window).on('resize', setCardHeights);
    // If content is loaded dynamically, you may want to call setCardHeights() again after updates
    // Auto-focus the last used new task input on page load (only if a task was just submitted)
    setTimeout(function() {
        let shouldFocus = localStorage.getItem('zenweek_should_focus');
        if (shouldFocus === 'true') {
            let lastInputName = localStorage.getItem('zenweek_last_task_input');
            let inputToFocus = null;
            if (lastInputName) {
                inputToFocus = document.querySelector(`input.createTask[name="taskname"][data-zenweek="${lastInputName}"]`);
            }
            if (!inputToFocus) {
                inputToFocus = document.querySelector('.createTask');
            }
            if (inputToFocus) {
                inputToFocus.focus();
            }
            // Clear the focus flag after focusing
            localStorage.removeItem('zenweek_should_focus');
        }
    }, 200);

    // On submit, store the unique identifier for the input field used and set focus flag
    $(document).on('submit', 'form.createTask123', function(e) {
        let input = $(this).find('input.createTask');
        if (input.length) {
            // Use a unique identifier: year+week+date (if present)
            let year = $(this).find('input[name="year"]').val();
            let week = $(this).find('input[name="week"]').val();
            let date = $(this).find('input[name="date"]').val() || '';
            let unique = `${year}_${week}_${date}`;
            localStorage.setItem('zenweek_last_task_input', unique);
            // Set flag that focus should be restored after page reload
            localStorage.setItem('zenweek_should_focus', 'true');
        }
        // After reload, focus will be restored to this field if a task was submitted
    });
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
                            $(dragging).remove();
                            // Reload page to update badges, or trigger badge update via AJAX if implemented
                            location.reload();
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
        // Add a unique data-zenweek attribute for identification
        let form = $(this).closest('form.createTask123');
        let year = form.find('input[name="year"]').val();
        let week = form.find('input[name="week"]').val();
        let date = form.find('input[name="date"]').val() || '';
        let unique = `${year}_${week}_${date}`;
        $(this).attr('data-zenweek', unique);
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
        var $li = $(this).parent();
        var $ul = $li.parent();
        var taskid = $li.attr("taskid");
        // Find the badge for the week that is both current and selected (green badge and selected)
        var badge = $(".btn-group .cw-button-selected .open-task-badge.bg-success");
        if ($(this).siblings("span").hasClass("task-done")) {
            $(this).siblings("span").removeClass("task-done");
            $(this).removeClass("bi-check-square");
            $(this).addClass("bi-square");
            editTask(taskid, "undo");
            // Increment badge
            if (badge.length) {
                var val = parseInt(badge.text(), 10) || 0;
                badge.text(val + 1);
            }
            // Move item up (before first done item)
            var $firstDone = $ul.children('li').filter(function() {
                return $(this).find('span.task-done').length > 0;
            }).first();
            if ($firstDone.length) {
                $li.insertBefore($firstDone);
            } else {
                $li.appendTo($ul);
            }
        } else {
            $(this).siblings("span").addClass("task-done");
            $(this).removeClass("bi-square");
            $(this).addClass("bi-check-square");
            editTask(taskid, "done");
            // Decrement badge
            if (badge.length) {
                var val = parseInt(badge.text(), 10) || 0;
                badge.text(Math.max(val - 1, 0));
            }
            // Move item to bottom
            $li.appendTo($ul);
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
