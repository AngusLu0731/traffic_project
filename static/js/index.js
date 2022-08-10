var lastScrollTop = 0;

window.addEventListener("scroll", function(){ 
   var st = window.pageYOffset || document.documentElement.scrollTop; 
   if (st > lastScrollTop){
      var box = document.getElementById('I-header');
      box.style.display="none";
   } else {
        var box = document.getElementById('I-header');
        box.style.display="flex";
   }
   lastScrollTop = st <= 0 ? 0 : st; // For Mobile or negative scrolling
}, false);







