$(document).ready(function() {
    const collect_sources_btn = $("#collect_sources_btn");
    const analyze_raw_data_btn = $("#analyze_raw_data_btn");
    const analyze_each_case_btn = $("#analyze_each_case_btn");
    const generate_daily_stats_btn = $("#generate_daily_stats_btn");

    function clear() {
        $("#pages_input").css("border", "2px inset");
        $("#page_error").text("")
        $("#last_command_name").text("-")
        $("#last_command_status").text("-")
    }
    collect_sources_btn.on("click", function() {
        clear()
        pages = $("#pages_input").val();
        if (pages && !isNaN(pages) && pages > 0) {
            if (pages > 1) {
                $("#last_command_name").text("Collect sources from the last " + pages + " pages")
            } else {
                $("#last_command_name").text("Collect sources from the last page")
            }
            $.get("collect_sources/" + pages + "/", function(data, status) {
                $("#last_command_status").text(status)
            });
        } else {
            $("#pages_input").css("border", "2px solid red");
            $("#page_error").text("The page input should be a number > 0")
        }
    });

    analyze_each_case_btn.on("click", function() {
        clear()
        $("#last_command_name").text("Analyze each case for today")
        $.get("analyze_each_case_today/", function(data, status) {
            $("#last_command_status").text(status)
        });
    });

    generate_daily_stats_btn.on("click", function() {
        clear()
        $("#last_command_name").text("Generate daily stats")
        $.get("generate_daily_stats/", function(data, status) {
            $("#last_command_status").text(status)
        });
    });
    analyze_raw_data_btn.on("click", function() {
        clear()
        $("#last_command_name").text("Analyze raw data for today")
        $.get("analyze_raw_data/", function(data, status) {
            $("#last_command_status").text(status)
        });
    });
});
