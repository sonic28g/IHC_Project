var gamesData;

        document.addEventListener("DOMContentLoaded", function() {
            // Função para carregar e processar os dados do arquivo JSON
            function loadJSON(callback) {
                var xobj = new XMLHttpRequest();
                xobj.overrideMimeType("application/json");
                xobj.open('GET', 'games.json', true);
                xobj.onreadystatechange = function() {
                    if (xobj.readyState == 4 && xobj.status == "200") {
                        callback(JSON.parse(xobj.responseText));
                    }
                };
                xobj.send(null);
            }

            // Função para renderizar os cartões de jogo
            function renderGameCards(games) {
                var container = document.getElementById("gameCardsContainer");
                container.innerHTML = ""; // Limpa o conteúdo atual do container

                games.forEach(function(game) {
                    var card = document.createElement("div");
                    card.classList.add("col-md-4");
                    card.innerHTML = `
                        <div class="card">
                            <img src="img/${game.title.replace(/\s+/g, '').toLowerCase()}.jpg" class="card-img-top" alt="${game.title}">
                            <div class="card-body">
                                <h5 class="card-title">${game.title}</h5>
                                <p class="card-text">$${game.price}</p>
                                <a href="#" class="btn btn-primary">Buy Now</a>
                            </div>
                        </div>
                    `;
                    container.appendChild(card);
                });
            }

            // Carregar e processar os dados do arquivo JSON e, em seguida, renderizar os cartões de jogo
            loadJSON(function(response) {
                gamesData = response; // Atribuir os dados carregados à variável global
                renderGameCards(gamesData);
                // Preencher as opções do seletor de gênero
                var genreSelect = document.getElementById("genreSelect");
                var genres = [];
                gamesData.forEach(function(game) {
                    game.genre.forEach(function(genre) {
                        if (!genres.includes(genre)) {
                            genres.push(genre);
                            var option = document.createElement("option");
                            option.textContent = genre;
                            option.value = genre;
                            genreSelect.appendChild(option);
                        }
                    });
                });
            });

            // Event listener para o menu suspenso de ordenação
            var sortSelect = document.getElementById("sortSelect");
            sortSelect.addEventListener("change", function() {
                var sortBy = this.value;
                var selectedGenre = document.getElementById("genreSelect").value;
                if (selectedGenre === "Show All Genres") {
                    // Se "Show All Genres" for selecionado, ordenar todos os jogos
                    if (sortBy === "2") {
                        // Ordenar por preço
                        gamesData.sort(function(a, b) {
                            return a.price - b.price;
                        });
                    } else if (sortBy === "1") {
                        // Ordenar alfabeticamente
                        gamesData.sort(function(a, b) {
                            return a.title.localeCompare(b.title);
                        });
                    }
                    // Renderizar novamente os cartões de jogo com a nova ordem
                    renderGameCards(gamesData);
                } else {
                    // Filtrar os jogos com base no gênero selecionado
                    var filteredGames = gamesData.filter(function(game) {
                        return game.genre.includes(selectedGenre);
                    });
                    // Ordenar os jogos filtrados
                    if (sortBy === "2") {
                        // Ordenar por preço
                        filteredGames.sort(function(a, b) {
                            return a.price - b.price;
                        });
                    } else if (sortBy === "1") {
                        // Ordenar alfabeticamente
                        filteredGames.sort(function(a, b) {
                            return a.title.localeCompare(b.title);
                        });
                    }
                    // Renderizar os cartões de jogo filtrados e ordenados
                    renderGameCards(filteredGames);
                }
            });

            // Event listener para o seletor de gênero
            var genreSelect = document.getElementById("genreSelect");
            genreSelect.addEventListener("change", function() {
                var selectedGenre = this.value;
                var sortBy = document.getElementById("sortSelect").value;
                if (selectedGenre === "Show All Genres") {
                    // Se "Show All Genres" for selecionado, ordenar todos os jogos
                    if (sortBy === "2") {
                        // Ordenar por preço
                        gamesData.sort(function(a, b) {
                            return a.price - b.price;
                        });
                    } else if (sortBy === "1") {
                        // Ordenar alfabeticamente
                        gamesData.sort(function(a, b) {
                            return a.title.localeCompare(b.title);
                        });
                    }
                    // Renderizar novamente os cartões de jogo com a nova ordem
                    renderGameCards(gamesData);
                } else {
                    // Filtrar os jogos com base no gênero selecionado
                    var filteredGames = gamesData.filter(function(game) {
                        return game.genre.includes(selectedGenre);
                    });
                    // Ordenar os jogos filtrados
                    if (sortBy === "2") {
                        // Ordenar por preço
                        filteredGames.sort(function(a, b) {
                            return a.price - b.price;
                        });
                    } else if (sortBy === "1") {
                        // Ordenar alfabeticamente
                        filteredGames.sort(function(a, b) {
                            return a.title.localeCompare(b.title);
                        });
                    }
                    // Renderizar os cartões de jogo filtrados e ordenados
                    renderGameCards(filteredGames);
                }
            });
        });