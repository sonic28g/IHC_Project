var gamesData;

document.addEventListener("DOMContentLoaded", function () {
  // Load the JSON data
  function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open("GET", "/games", true);
    xobj.onreadystatechange = function () {
      if (xobj.readyState == 4 && xobj.status == "200") {
        callback(JSON.parse(xobj.responseText));
      }
    };
    xobj.send(null);
  }

  // Render the game cards
  function renderGameCards(games) {
    var container = document.getElementById("gameCardsContainer");
    container.innerHTML = "";
    var row;
    console.log(games);
    games.forEach(function (game, index) {
      if (index % 4 === 0) {
        row = document.createElement("div");
        row.classList.add("row", "d-flex", "justify-content-center");
        container.appendChild(row);
      }
      var card = document.createElement("div");
      card.classList.add("col-md-3", "mb-3");
      console.log(game);
      card.innerHTML = `
      <div class="card">
          <img src="${game[4]}" class="card-img-top" alt="${game[1]}">
          <div class="card-body">
              <h5 class="card-title">${game[1]}</h5>
              <p class="card-text">${game[2]}€</p>
              <a href="/game/${game[0]}" class="btn btn-primary">Buy Now</a>
          </div>
      </div>
  `;
      row.appendChild(card);
    });
  }

  // Load the games data
  loadJSON(function (response) {
    gamesData = response;
    renderGameCards(gamesData);
  });

  // Search games
  function searchGames(title, callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open("GET", "/search/" + title, true);
    console.log(xobj);
    xobj.onreadystatechange = function () {
      if (xobj.readyState == 4 && xobj.status == "200") {
        callback(JSON.parse(xobj.responseText));
      }
    };
    xobj.send(null);
  }

  // Search games
  var searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("input", function () {
    var enteredTitle = this.value;
    searchGames(enteredTitle, function (response) {
      gamesData = response;
      renderGameCards(gamesData);
    });
  });

  // Sort games
  function sortGames(sortOption) {
    if (sortOption === "1") {
      // Sort by title (alphabetical order)
      gamesData.sort(function (a, b) {
        var titleA = a[1].toUpperCase();
        var titleB = b[1].toUpperCase();
        if (titleA < titleB) {
          return -1;
        }
        if (titleA > titleB) {
          return 1;
        }
        return 0;
      });
    } else if (sortOption === "2") {
      // Sort by price
      gamesData.sort(function (a, b) {
        return a[2] - b[2];
      });
    }
    renderGameCards(gamesData);
  }

  // Add event listener to sort select
  var sortSelect = document.getElementById("sortSelect");
  sortSelect.addEventListener("change", function () {
    sortGames(this.value);
  });

  // Extract all unique genres from the games data
  function getAllGenres() {
    var allGenres = new Set();
    gamesData.forEach(function (game) {
      var genres = game[3];
      genres.forEach(function (genre) {
        allGenres.add(genre);
      });
    });
    return Array.from(allGenres);
  }

  // Add genre options to genreSelect
  function showAllGenres() {
    var allGenres = getAllGenres();
    var genreSelect = document.getElementById("genreSelect");
    allGenres.forEach(function (genre) {
      var option = document.createElement("option");
      option.value = genre;
      option.text = genre;
      genreSelect.appendChild(option);
    });
  }

  // Load the games data
  loadJSON(function (response) {
    gamesData = response;
    renderGameCards(gamesData);
    showAllGenres();
  });

  // Filter games by genre
  function filterGamesByGenre(genre) {
    var filteredGames = gamesData.filter(function (game) {
      return game[3].includes(genre);
    });
    renderGameCards(filteredGames);
  }

  // Add event listener to genreSelect
  var genreSelect = document.getElementById("genreSelect");
  genreSelect.addEventListener("change", function () {
    filterGamesByGenre(this.value);
  });
});

