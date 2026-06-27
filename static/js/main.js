document.addEventListener('DOMContentLoaded', function() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    const songsContainer = document.getElementById('songs-container');
    const loadingIndicator = document.getElementById('loading-indicator');

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            const nextPage = this.dataset.nextPage;
            loadMoreBtn.style.display = 'none';
            loadingIndicator.style.display = 'block';

            fetch(`/load-more/?page=${nextPage}`)
                .then(response => response.json())
                .then(data => {
                    loadingIndicator.style.display = 'none';
                    
                    if (data.songs && data.songs.length > 0) {
                        data.songs.forEach(song => {
                            const html = createSongHTML(song);
                            songsContainer.insertAdjacentHTML('beforeend', html);
                        });

                        if (data.has_next) {
                            loadMoreBtn.style.display = 'inline-block';
                            loadMoreBtn.dataset.nextPage = data.next_page;
                        }
                    }
                })
                .catch(error => {
                    loadingIndicator.style.display = 'none';
                    loadMoreBtn.style.display = 'inline-block';
                    console.error('Error loading more songs:', error);
                });
        });
    }

    function createSongHTML(song) {
        let starsHTML = '';
        const fullStars = song.star_rating || 0;
        
        for (let i = 1; i <= 10; i++) {
            const isFilled = i <= fullStars;
            starsHTML += `<i class="bi bi-star${isFilled ? '-fill' : ''}" 
                               style="color: ${isFilled ? 'gold' : '#ddd'};"></i>`;
        }

        const coverHTML = song.cover_image 
            ? `<img src="${song.cover_image}" alt="${song.title}" class="rounded-circle" style="width: 80px; height: 80px; object-fit: cover;">`
            : `<div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center" style="width: 80px; height: 80px;">
                <i class="bi bi-music-note text-white" style="font-size: 2rem;"></i>
               </div>`;

        const isAuthenticated = document.querySelector('.navbar .nav-link') !== null;
        const detailsButton = isAuthenticated 
            ? `<a href="/song/${song.id}/" class="btn btn-outline-primary btn-sm">
                    <i class="bi bi-eye"></i> Детали
               </a>`
            : `<span class="text-muted small" title="Войдите для просмотра">
                    <i class="bi bi-lock"></i> 
               </span>`;

        return `
            <div class="song-item" data-song-id="${song.id}">
                <div class="row align-items-center py-3 border-bottom">
                    <div class="col-auto">
                        ${coverHTML}
                    </div>
                    <div class="col-md-3">
                        <h5 class="mb-0">${song.title}</h5>
                        <small class="text-muted">${song.artist}</small>
                    </div>
                    <div class="col-md-2">
                        <span class="badge bg-info">${song.genre}</span>
                    </div>
                    <div class="col-md-2 text-center">
                        <div class="rating-display">
                            <span class="h4 mb-0">${song.rating.toFixed(1)}/10</span>
                            <div class="stars">
                                ${starsHTML}
                            </div>
                            <small class="text-muted">Голосов: ${song.total_votes}</small>
                        </div>
                    </div>
                    <div class="col-md-1 text-center">
                        <span class="badge bg-secondary">${song.release_year}</span>
                    </div>
                    <div class="col-md-2 text-end">
                        ${detailsButton}
                    </div>
                </div>
            </div>
        `;
    }

    const voteStars = document.querySelectorAll('.vote-stars .bi-star');
    if (voteStars.length > 0) {
        voteStars.forEach(star => {
            star.addEventListener('click', function() {
                const value = parseInt(this.dataset.value);
                const container = this.closest('.vote-stars');
                const submitBtn = document.getElementById('submit-vote-btn');
                
                container.querySelectorAll('.bi-star, .bi-star-fill').forEach(s => {
                    const v = parseInt(s.dataset.value);
                    if (v <= value) {
                        s.className = 'bi bi-star-fill';
                        s.style.color = 'gold';
                    } else {
                        s.className = 'bi bi-star';
                        s.style.color = '#ddd';
                    }
                });
                
                submitBtn.dataset.rating = value;
                submitBtn.disabled = false;
            });
        });
    }

    const submitVoteBtn = document.getElementById('submit-vote-btn');
    if (submitVoteBtn) {
        submitVoteBtn.addEventListener('click', function() {
            const rating = this.dataset.rating;
            const songId = this.dataset.songId;
            
            if (!rating) {
                alert('Выберите оценку!');
                return;
            }

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
            
            fetch(`/song/${songId}/vote/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ rating: rating })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message || 'Голос учтен!');
                    location.reload();
                } else {
                    alert(data.error || 'Произошла ошибка');
                }
            })
            .catch(error => {
                alert('Ошибка при голосовании');
            });
        });
    }
});