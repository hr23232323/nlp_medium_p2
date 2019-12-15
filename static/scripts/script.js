$("#input-form").submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function (data) {
            //console.log(data); // show response from the php script.
            var pred_image = $("#pred_image");
            var slide_div = $("#slide-div");
            var img_path = ""
            if (data == 'n') {
                img_path = "static/img/sad.webp"
            } else if (data == 'p') {
                img_path = "static/img/happy.webp"
            } else {
                console.log("SOMETHING BROKE")
            }

            // First run, edge case
            if (slide_div.is(":hidden")) {
                pred_image.attr("src", img_path);
            };

            slide_div.slideToggle('slow', function () {
                if ($(this).is(":hidden")) {
                    $(this).slideToggle('slow')
                    pred_image.attr("src", img_path);
                };
            });
        }
    });
});


$("#save-form").submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var val = $("button[type=submit][clicked=true]").val();
    var form = $(this)
    var url = form.attr('action');

    //form = form.serializeArray();
    var formData = {
        "save_type": val
    }

    $.ajax({
        type: "POST",
        url: url,
        data: formData, // serializes the form's elements.
        success: function (data) {
            var conf_text = $("#confirmation_text");
            conf_text.text(data);
            conf_text.fadeIn(100);
            conf_text.delay(2000).fadeOut()
        }
    });
});

$("#save-form button[type=submit]").click(function () {
    $("button[type=submit]", $(this).parents("#save-form")).removeAttr("clicked");
    $(this).attr("clicked", "true");
});
