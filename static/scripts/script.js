// Override defaiult behavior for input prediction submission using jquery and AJAX
$("#input-form").submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function (data) {
            var pred_image = $("#pred_image");
            var slide_div = $("#slide-div");

            // Path to image to display as output
            var img_path = ""
            if (data == 'n') {
                img_path = "static/img/sad.webp"
            } else if (data == 'p') {
                img_path = "static/img/happy.webp"
            } else {
                console.log("SOMETHING BROKE")
            }

            // First run, edge case of sliding div
            if (slide_div.is(":hidden")) {
                pred_image.attr("src", img_path);
            };

            // Toggle div showing for every subsequent run
            slide_div.slideToggle('slow', function () {
                if ($(this).is(":hidden")) {
                    $(this).slideToggle('slow')
                    pred_image.attr("src", img_path);
                };
            });
        }
    });
});

// Override defaiult behavior for user feedback submission using jquery and AJAX
$("#save-form").submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    // Get what button was pressed (correct/incorrect)
    var val = $("button[type=submit][clicked=true]").val();
    var form = $(this)
    var url = form.attr('action');

    // Attach user feedback choice to form 
    var formData = {
        "save_type": val
    }

    // Ajax method to process request in page instead of reloading
    $.ajax({
        type: "POST",
        url: url,
        data: formData, // Previously attached user data
        success: function (data) {
            // Show confirmation text
            var conf_text = $("#confirmation_text");
            conf_text.text(data);
            conf_text.fadeIn(100);

            // Fade out
            conf_text.delay(2000).fadeOut()
        }
    });
});

// Manually attach attribute to feedback buttons to capture which one user clicked
$("#save-form button[type=submit]").click(function () {
    $("button[type=submit]", $(this).parents("#save-form")).removeAttr("clicked");
    $(this).attr("clicked", "true");
});
