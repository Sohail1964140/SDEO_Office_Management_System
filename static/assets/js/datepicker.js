$(function() {
  'use strict';

  if($('.datepicker').length) {
    var date = new Date();
    var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    $('.datepicker').datepicker({
      format: "mm/dd/yyyy",
      todayHighlight: true,
      autoclose: true,
    });
    $('.datepicker').datepicker('setDate', today);
    $('.datepicker').datepicker('max', today);
  }
});