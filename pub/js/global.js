function includeHTML() {
    var z, i, elmnt, file, xhttp;
    /* Loop through a collection of all HTML elements: */
    z = document.getElementsByTagName("*");
    for (i = 0; i < z.length; i++) {
      elmnt = z[i];
      /* search for elements with a certain attribute: */
      file = elmnt.getAttribute("loadhtml");
      if (file) {
        var requestUrl = file;
        // If testing on localhost/127.0.0.1, convert absolute brijesh.work domain to relative path fallback for CORS/offline support
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
          if (file.indexOf("https://brijesh.work/") === 0) {
            var relativePath = file.replace("https://brijesh.work/", "");
            var locPath = window.location.pathname;
            var repoIdx = locPath.indexOf("/github/brijeshwork.github.io/");
            if (repoIdx !== -1) {
              requestUrl = locPath.substring(0, repoIdx) + "/github/brijeshwork.github.io/" + relativePath;
            } else {
              requestUrl = "/" + relativePath;
            }
          }
        }
        /* Make an HTTP request using the attribute value as the file name: */
        xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState == 4) {
            if (this.status == 200) {
              elmnt.innerHTML = this.responseText;
            } else if (this.status == 404 || this.status == 0) {
              // Fallback to original file URL if local relative path fails
              if (requestUrl !== file) {
                var fallbackXhttp = new XMLHttpRequest();
                fallbackXhttp.onreadystatechange = function() {
                  if (this.readyState == 4 && this.status == 200) {
                    elmnt.innerHTML = this.responseText;
                  }
                };
                fallbackXhttp.open("GET", file, true);
                fallbackXhttp.send();
              } else {
                elmnt.innerHTML = "Page not found.";
              }
            }
            /* Remove the attribute, and call this function once more: */
            elmnt.removeAttribute("loadhtml");
            includeHTML();
          }
        }
        xhttp.open("GET", requestUrl, true);
        xhttp.send();
        /* Exit the function: */
        return;
    }
  }

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", includeHTML);
} else {
  includeHTML();
}

(function(c,l,a,r,i,t,y){
c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
})(window, document, "clarity", "script", "dplzzvc2xo");