function searchMovie() {
  var movieInput = document.getElementById("movieInput").value;
  if (movieInput.trim() !== "") {
      // Display loading spinner while fetching data
      $("#loading").show();

      // Make an AJAX request to the server with the search query
      $.ajax({
          type: "POST",
          url: "/search_movies",
          data: { query: movieInput },
          success: function (data) {
              // Hide loading spinner
              $("#loading").hide();

              // Display search results
              $("#movieDetails").html(data);

              // Additional code for integrating recommendations (part 1)
              $(".movie-result").on("click", function () {
                  var movieId = $(this).data("movie-id");
                  getRecommendations(movieId);
              });
          },
          error: function () {
              // Hide loading spinner and show an error message
              $("#loading").hide();
              $("#movieDetails").html("<p>Error fetching data. Please try again.</p>");
          }
      });
  }
}

function getRecommendations(movieId) {
  // Display loading spinner while fetching recommendations
  $("#loading").show();

  // Make an AJAX request to the server with the selected movie ID
  $.ajax({
      type: "POST",
      url: "/get_recommendations",
      data: { movieId: movieId },
      success: function (data) {
          // Hide loading spinner
          $("#loading").hide();

          // Display recommendations
          $("#recommendations").html(data);
      },
      error: function () {
          // Hide loading spinner and show an error message
          $("#loading").hide();
          $("#recommendations").html("<p>Error fetching recommendations. Please try again.</p>");
      }
  });
}

var width = $(window).width();
window.onscroll = function () {
  if (width >= 1000) {
      if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
          $("#header").css({
              background: "#fff",
              color: "#000",
              "box-shadow": "0px 0px 20px rgba(0,0,0,0.09)",
              padding: "4vh 4vw"
          });
          $("#navigation a").hover(function () {
              $(this).css("border-bottom", "2px solid rgb(255, 44, 90)");
          }, function () {
              $(this).css("border-bottom", "2px solid transparent");
          });
      } else {
          $("#header").css({
              background: "transparent",
              color: "#fff",
              "box-shadow": "0px 0px 0px rgba(0,0,0,0)",
              padding: "6vh 4vw"
          });
          $("#navigation a").hover(function () {
              $(this).css("border-bottom", "2px solid #fff");
          }, function () {
              $(this).css("border-bottom", "2px solid transparent");
          });
      }
  }
};

function magnify(imglink) {
  $("#img_here").css("background", `url('${imglink}') center center`);
  $("#magnify").css("display", "flex").addClass("animated fadeIn");
  setTimeout(function () {
      $("#magnify").removeClass("animated fadeIn");
  }, 800);
}

function closemagnify() {
  $("#magnify").addClass("animated fadeOut");
  setTimeout(function () {
      $("#magnify").css("display", "none").removeClass("animated fadeOut");
      $("#img_here").css("background", `url('') center center`);
  }, 800);
}

setTimeout(function () {
  $("#loading").addClass("animated fadeOut");
  setTimeout(function () {
      $("#loading").removeClass("animated fadeOut").css("display", "none");
  }, 800);
}, 1650);

$(document).ready(function () {
  $("a").on('click', function (event) {
      if (this.hash !== "") {
          event.preventDefault();
          var hash = this.hash;
          $('body,html').animate({
              scrollTop: $(hash).offset().top
          }, 1800, function () {
              window.location.hash = hash;
          });
      }
  });
});

// Event delegation for dynamically added elements
$(document).on("click", ".movie-result", function () {
  var movieId = $(this).data("movie-id");
  getRecommendations(movieId);
});
