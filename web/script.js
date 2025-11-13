document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('downloadForm');
    const status = document.getElementById('status');
    const previewDiv = document.getElementById('preview');
    const downloadLinks = document.getElementById('downloadLinks');
    const pasteBtn = document.getElementById('pasteBtn');
    const igUrlInput = document.getElementById('igUrl');

    console.log('Form:', form ? 'Found' : 'Missing');
    console.log('Status:', status ? 'Found' : 'Missing');
    console.log('Preview:', previewDiv ? 'Found' : 'Missing');
    console.log('DownloadLinks:', downloadLinks ? 'Found' : 'Missing');

    if (!form || !status || !previewDiv || !downloadLinks) {
        console.error('Missing DOM elements—check IDs in index.html');
        return;
    }

    if (pasteBtn && igUrlInput) {
        pasteBtn.addEventListener('click', async function() {
            try {
                const text = await navigator.clipboard.readText();
                if (text) {
                    igUrlInput.value = text;
                    igUrlInput.focus();
                    const originalText = pasteBtn.textContent;
                    pasteBtn.textContent = '✓';
                    pasteBtn.style.backgroundColor = '#27ae60';
                    setTimeout(() => {
                        pasteBtn.textContent = originalText;
                        pasteBtn.style.backgroundColor = '#3498db';
                    }, 1000);
                }
            } catch (err) {
                console.error('Failed to read clipboard:', err);
                igUrlInput.focus();
                document.execCommand('paste');
            }
        });
    }

    function showNewDownloadButton() {
        const newDownloadBtn = document.createElement('button');
        newDownloadBtn.id = 'newDownloadBtn';
        newDownloadBtn.textContent = 'Download Another';
        newDownloadBtn.className = 'new-download-btn';
        newDownloadBtn.onclick = function() {
            form.classList.remove('hidden');
            igUrlInput.value = '';
            previewDiv.innerHTML = '';
            downloadLinks.innerHTML = '';
            status.textContent = '';
            status.className = '';
            status.style.display = 'none';
            newDownloadBtn.remove();
            igUrlInput.focus();
        };
        previewDiv.parentNode.insertBefore(newDownloadBtn, previewDiv);
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const igUrl = document.getElementById('igUrl').value.trim();
        if (!igUrl) {
            status.textContent = 'Enter a URL';
            return;
        }

        console.log('Submit started for URL:', igUrl);

        form.classList.add('hidden');

        status.className = 'status loading';
        status.textContent = 'Downloading preview...';
        status.style.display = 'block';
        previewDiv.innerHTML = '';
        downloadLinks.innerHTML = '';

        const shortcode = extractShortcode(igUrl);
        console.log('Extracted shortcode:', shortcode);

        if (!shortcode) {
            status.className = 'status error';
            status.textContent = 'Invalid URL—no shortcode found';
            status.style.display = 'block';
            form.classList.remove('hidden');
            return;
        }

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 500000);

        try {
            console.log('Downloading at /api/v1/download?shortcode=' + shortcode + '...');
            const downloadResponse = await fetch(`/api/v1/download?shortcode=${shortcode}`, { signal: controller.signal });
            clearTimeout(timeoutId);

            if (!downloadResponse.ok) {
                const errorText = await downloadResponse.text();
                throw new Error(`Download failed: ${downloadResponse.status} - ${errorText.substring(0, 100)}`);
            }
            const data = await downloadResponse.json();
            console.log('Download data:', data);

            if (data.cached) {
                status.className = 'status success';
                status.style.display = 'block';
                status.textContent = 'Using previously downloaded files (cached)';
                setTimeout(() => {
                    status.style.display = 'none';
                }, 2000);
            } else {
                status.style.display = 'none';
            }

            function isVideoFile(file) {
                const videoExtensions = ['mp4', 'mov', 'webm', 'avi', 'mkv'];
                return videoExtensions.includes(file.type?.toLowerCase()) || 
                       file.name?.toLowerCase().endsWith('.mp4') ||
                       file.name?.toLowerCase().endsWith('.mov') ||
                       file.name?.toLowerCase().endsWith('.webm');
            }

            function createMediaElement(file, thumbnailUrl = null) {
                if (isVideoFile(file)) {
                    const video = document.createElement('video');
                    video.style.display = 'block';
                    video.style.maxWidth = '100%';
                    video.style.height = 'auto';
                    video.style.margin = '0 auto';
                    video.controls = true;
                    video.preload = 'metadata';
                    
                    if (thumbnailUrl) {
                        video.poster = thumbnailUrl;
                        console.log('Setting video poster to:', thumbnailUrl);
                    }
                    
                    if (file.path) {
                        video.src = file.path;
                        console.log('Setting video src to:', file.path);
                    }
                    
                    video.onerror = function() {
                        console.error('Failed to load video from:', video.src);
                    };
                    
                    video.onloadedmetadata = function() {
                        console.log('Video metadata loaded successfully from:', video.src);
                    };
                    
                    return video;
                } else {
                    const img = document.createElement('img');
                    img.alt = 'Post Preview';
                    img.loading = 'lazy';
                    img.style.display = 'block';
                    img.style.maxWidth = '100%';
                    img.style.height = 'auto';
                    img.style.margin = '0 auto';
                    
                    img.onerror = function() {
                        console.error('Failed to load image from:', img.src);
                        img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjRmNGY0Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzMzMyIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIFByZXZpZXc8L3RleHQ+PC9zdmc+';
                    };
                    
                    img.onload = function() {
                        console.log('Image loaded successfully from:', img.src);
                    };
                    
                    if (file.path) {
                        img.src = file.path;
                        console.log('Setting image src to:', file.path);
                    } else {
                        console.warn('No path in file data:', file);
                        img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjRmNGY0Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzMzMyIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIFByZXZpZXc8L3RleHQ+PC9zdmc+';
                    }
                    
                    return img;
                }
            }

            const firstFile = data.files[0];
            console.log('First file for preview:', firstFile);

            const thumbDiv = document.createElement('div');
            thumbDiv.className = 'media-item';
            
            const mediaElement = createMediaElement(firstFile, data.preview_thumbnail);
            
            const btn = document.createElement('button');
            btn.textContent = `Download ${isVideoFile(firstFile) ? 'Video' : 'Image'}`;
            btn.onclick = () => downloadFile(firstFile.path, firstFile.name);
            
            thumbDiv.appendChild(mediaElement);
            thumbDiv.appendChild(btn);
            previewDiv.appendChild(thumbDiv);
            
            console.log('Rendered preview with media element in DOM');

            if (data.files.length > 1) {
                const grid = document.createElement('div');
                grid.className = 'media-grid';
                data.files.slice(1).forEach((file, index) => {
                    console.log('Rendering additional file ' + (index + 2));
                    const extraDiv = document.createElement('div');
                    extraDiv.className = 'media-item';
                    
                    const extraMediaElement = createMediaElement(
                        file, 
                        isVideoFile(file) ? data.preview_thumbnail : null
                    );
                    
                    const extraBtn = document.createElement('button');
                    extraBtn.textContent = `Download ${isVideoFile(file) ? 'Video' : 'Image'}`;
                    extraBtn.onclick = () => downloadFile(file.path, file.name);
                    
                    extraDiv.appendChild(extraMediaElement);
                    extraDiv.appendChild(extraBtn);
                    grid.appendChild(extraDiv);
                });
                previewDiv.appendChild(grid);
            }

            showNewDownloadButton();

            console.log('Downloads complete—preview rendered from local files.');

        } catch (error) {
            clearTimeout(timeoutId);
            console.error('Submit error:', error);
            status.className = 'status error';
            status.style.display = 'block';
            status.textContent = `Error: ${error.name === 'AbortError' ? 'Timeout (30s)' : error.message}`;
            form.classList.remove('hidden');
            showNewDownloadButton();
        }
    });

    function extractShortcode(url) {
        const parsed = new URL(url);
        let path = parsed.pathname;
        if (path.includes('/p/')) {
            return path.split('/p/')[1].split('/')[0];
        } else if (path.includes('/reel/')) {
            return path.split('/reel/')[1].split('/')[0];
        }
        return '';
    }

    function downloadFile(path, name) {
        console.log('Downloading:', name);
        const link = document.createElement('a');
        link.href = path;
        link.download = name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});
