/**
 * Travolozza - Frontend JavaScript
 * Handles UI interactivity and communication with Python backend via Eel
 */

// Store image data
const imageStore = [];

// DOM Elements
const imageList = document.getElementById('image-list');
const textBlocks = document.getElementById('text-blocks');
const addImageBtn = document.getElementById('add-image-btn');
const addBlockBtn = document.getElementById('add-block-btn');
const copyBtn = document.getElementById('copy-btn');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Add initial text block
    addTextBlock();

    // Event listeners
    addImageBtn.addEventListener('click', handleAddImages);
    addBlockBtn.addEventListener('click', () => addTextBlock());
    copyBtn.addEventListener('click', handleCopy);
});

/**
 * Handle adding images via Python file dialog
 */
async function handleAddImages() {
    try {
        const images = await eel.select_images()();
        images.forEach(img => {
            imageStore.push(img);
            renderImageThumbnail(img);
        });
    } catch (error) {
        console.error('Error selecting images:', error);
    }
}

/**
 * Render an image thumbnail in the header
 */
function renderImageThumbnail(imageData) {
    const div = document.createElement('div');
    div.className = 'image-thumbnail';
    div.dataset.path = imageData.path;

    const img = document.createElement('img');
    img.src = imageData.data;
    img.alt = 'Context image';

    const removeBtn = document.createElement('button');
    removeBtn.className = 'remove-btn';
    removeBtn.innerHTML = '×';
    removeBtn.title = 'Remove image';
    removeBtn.addEventListener('click', () => removeImage(imageData.path, div));

    div.appendChild(img);
    div.appendChild(removeBtn);
    imageList.appendChild(div);
}

/**
 * Remove an image from the store and DOM
 */
function removeImage(path, element) {
    const index = imageStore.findIndex(img => img.path === path);
    if (index > -1) {
        imageStore.splice(index, 1);
    }
    element.remove();
}

/**
 * Add a new text block to the prompt zone
 */
function addTextBlock(placeholder = 'Write your prompt here...') {
    const blockCount = textBlocks.children.length;
    
    const div = document.createElement('div');
    div.className = 'text-block';

    const textarea = document.createElement('textarea');
    textarea.placeholder = blockCount === 0 
        ? 'Write your main instruction here...' 
        : `Block ${blockCount + 1}: Additional context, examples, format...`;
    
    // Auto-resize textarea
    textarea.addEventListener('input', () => autoResize(textarea));

    const removeBtn = document.createElement('button');
    removeBtn.className = 'remove-btn';
    removeBtn.innerHTML = '×';
    removeBtn.title = 'Remove block';
    removeBtn.addEventListener('click', () => removeTextBlock(div));

    div.appendChild(textarea);
    div.appendChild(removeBtn);
    textBlocks.appendChild(div);

    // Focus the new textarea
    textarea.focus();
}

/**
 * Auto-resize textarea based on content
 */
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

/**
 * Remove a text block
 */
function removeTextBlock(element) {
    // Keep at least one block
    if (textBlocks.children.length > 1) {
        element.remove();
    }
}

/**
 * Handle copy button click - send data to Python
 */
async function handleCopy() {
    // Collect all text from blocks
    const texts = Array.from(textBlocks.querySelectorAll('textarea'))
        .map(ta => ta.value)
        .filter(text => text.trim());

    // Collect image paths
    const imagePaths = imageStore.map(img => img.path);

    // Check if there's content to copy
    if (texts.length === 0 && imagePaths.length === 0) {
        showCopyFeedback(false, 'Nothing to copy!');
        return;
    }

    try {
        const result = await eel.copy_to_clipboard(texts, imagePaths)();
        
        if (result.success) {
            showCopyFeedback(true, result.warning || 'Copied!');
        } else {
            showCopyFeedback(false, result.error || 'Copy failed');
        }
    } catch (error) {
        console.error('Copy error:', error);
        showCopyFeedback(false, 'Copy failed');
    }
}

/**
 * Show visual feedback on copy button
 */
function showCopyFeedback(success, message) {
    const originalText = copyBtn.textContent;

    copyBtn.classList.add(success ? 'success' : 'error');
    copyBtn.textContent = success ? 'Copied!' : 'Failed';

    setTimeout(() => {
        copyBtn.classList.remove('success', 'error');
        copyBtn.textContent = originalText;
    }, 1500);
}

