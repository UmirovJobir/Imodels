
tinymce.init({
    // make sure you do not have `selector` defined here.
    mode: "none",
  });
  
  (function ($) {
    $(document).ready(function () {
      $(".djn-inline-form:not(.grp-empty-form) textarea").each(function () {
        // initialize MCE manually here rather than in `init` call.
        tinyMCE.execCommand("mceAddControl", false, this.id);
      });
    });
  })(django.jQuery || window.jQuery);
  
  (function ($) {
    $(document).on("formset:added", function (event, $form) {
      // initialize MCE manually when new formset is added
      $(".djn-inline-form:not(.grp-empty-form) textarea").each(function () {
        tinyMCE.execCommand("mceAddControl", false, this.id);
      });
    });
  })(django.jQuery);