/* Credit -  jQuery code snippet for Materialize CSS Initialization for each component/feature 
used during development borrowed from https://materializecss.com/
*/
$(document).ready(function () {
    $(".sidenav").sidenav({ edge: "right" });
    $(".collapsible").collapsible();
    $("select").formSelect();
    $(".carousel").carousel();
    $(".modal").modal();

    /* Credit - vanilla JavaScript code snippet for Materialize CSS Initialization for form validation
    borrowed from Task Manager Walkthrough Mini Project CI  */
    validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = { "border-bottom": "1px solid #3d5afe", "box-shadow": "0 1px 0 0 #3d5afe" };
        let classInvalid = { "border-bottom": "1px solid #f50057", "box-shadow": "0 1px 0 0 #f50057" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ display: "block", height: "0", padding: "0", width: "0", position: "absolute" });
        }
        $(".select-wrapper input.select-dropdown")
            .on("focusin", function () {
                $(this)
                    .parent(".select-wrapper")
                    .on("change", function () {
                        if (
                            $(this)
                                .children("ul")
                                .children("li.selected:not(.disabled)")
                                .on("click", function () {})
                        ) {
                            $(this).children("input").css(classValid);
                        }
                    });
            })
            .on("click", function () {
                if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(252,228,236,1.00)") {
                    $(this).parent(".select-wrapper").children("input").css(classValid);
                } else {
                    $(".select-wrapper input.select-dropdown").on("focusout", function () {
                        if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                            if ($(this).css("border-bottom") != "1px solid rgb(61, 90, 254)") {
                                $(this).parent(".select-wrapper").children("input").css(classInvalid);
                            }
                        }
                    });
                }
            });
    }
});