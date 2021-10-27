$(function () {
    $(".my-datepicker").datepicker(
      $.datepicker.regional["es"], "option", "dateFormat", "dd/mm/yy"
    );
  });