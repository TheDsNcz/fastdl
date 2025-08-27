// Plugin Community JavaScript

// Sample data for demonstration
let plugins = [
    {
        id: 1,
        name: "Admin ESP",
        author: "DevCS",
        category: "admin",
        description: "Plugin que permite aos administradores verem através das paredes para detectar cheaters e monitorar jogadores.",
        tags: ["admin", "esp", "wallhack", "anticheat"],
        version: "2.1",
        downloads: 1250,
        rating: 4.8,
        date: "2024-01-15",
        fileSize: "15 KB",
        screenshots: ["screenshot1.jpg", "screenshot2.jpg"]
    },
    {
        id: 2,
        name: "Ultimate Weapons",
        author: "WeaponMaster",
        category: "weapons",
        description: "Adiciona novas armas customizadas com efeitos especiais, sons únicos e balanceamento aprimorado.",
        tags: ["weapons", "custom", "effects", "sounds"],
        version: "3.0",
        downloads: 2100,
        rating: 4.9,
        date: "2024-01-12",
        fileSize: "45 KB",
        screenshots: ["weapon1.jpg", "weapon2.jpg"]
    },
    {
        id: 3,
        name: "Enhanced HUD",
        author: "UIDesigner",
        category: "hud",
        description: "Interface modernizada com informações detalhadas, mini-mapa melhorado e indicadores visuais aprimorados.",
        tags: ["hud", "interface", "minimap", "visual"],
        version: "1.5",
        downloads: 890,
        rating: 4.6,
        date: "2024-01-10",
        fileSize: "28 KB",
        screenshots: ["hud1.jpg", "hud2.jpg"]
    },
    {
        id: 4,
        name: "Fun Commands",
        author: "FunMaker",
        category: "fun",
        description: "Comandos divertidos para deixar o servidor mais animado: slap, rocket, freeze, glow e muito mais!",
        tags: ["fun", "commands", "entertainment", "server"],
        version: "2.3",
        downloads: 1680,
        rating: 4.7,
        date: "2024-01-08",
        fileSize: "22 KB",
        screenshots: ["fun1.jpg", "fun2.jpg"]
    },
    {
        id: 5,
        name: "Map Manager Pro",
        author: "MapperPro",
        category: "maps",
        description: "Sistema avançado de gerenciamento de mapas com votação automática, rotação personalizada e estatísticas.",
        tags: ["maps", "rotation", "voting", "management"],
        version: "4.1",
        downloads: 756,
        rating: 4.5,
        date: "2024-01-05",
        fileSize: "38 KB",
        screenshots: ["map1.jpg", "map2.jpg"]
    },
    {
        id: 6,
        name: "Gameplay Enhancer",
        author: "GameDev",
        category: "gameplay",
        description: "Melhorias na jogabilidade incluindo headshot sounds, killstreak rewards, e sistema de ranks.",
        tags: ["gameplay", "sounds", "rewards", "ranks"],
        version: "1.8",
        downloads: 1340,
        rating: 4.4,
        date: "2024-01-03",
        fileSize: "31 KB",
        screenshots: ["game1.jpg", "game2.jpg"]
    }
];

// DOM Elements
const pluginsGrid = document.getElementById('pluginsGrid');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortFilter = document.getElementById('sortFilter');
const uploadForm = document.getElementById('uploadForm');
const fileDropZone = document.getElementById('fileDropZone');
const pluginFile = document.getElementById('pluginFile');
const filePreview = document.getElementById('filePreview');
const modal = document.getElementById('pluginModal');
const modalContent = document.getElementById('modalContent');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    updateStats();
    renderPlugins(plugins);
    setupEventListeners();
    setupNavigation();
});

// Update statistics in hero section
function updateStats() {
    const totalPlugins = plugins.length;
    const totalDownloads = plugins.reduce((sum, plugin) => sum + plugin.downloads, 0);
    const totalUsers = Math.floor(totalDownloads / 3); // Estimate

    document.getElementById('totalPlugins').textContent = totalPlugins.toLocaleString();
    document.getElementById('totalDownloads').textContent = totalDownloads.toLocaleString();
    document.getElementById('totalUsers').textContent = totalUsers.toLocaleString();
}

// Render plugins in the grid
function renderPlugins(pluginsToRender) {
    if (pluginsToRender.length === 0) {
        pluginsGrid.innerHTML = '<div class="loading"><p>Nenhum plugin encontrado.</p></div>';
        return;
    }

    pluginsGrid.innerHTML = pluginsToRender.map(plugin => `
        <div class="plugin-card" onclick="openPluginModal(${plugin.id})">
            <div class="plugin-header">
                <div class="plugin-title">${plugin.name}</div>
                <div class="plugin-author">por ${plugin.author}</div>
                <span class="plugin-category">${getCategoryName(plugin.category)}</span>
            </div>
            <div class="plugin-content">
                <div class="plugin-description">${plugin.description}</div>
                <div class="plugin-tags">
                    ${plugin.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
            <div class="plugin-footer">
                <div class="plugin-stats">
                    <span><i class="fas fa-download"></i> ${plugin.downloads.toLocaleString()}</span>
                    <span><i class="fas fa-star"></i> ${plugin.rating}</span>
                    <span><i class="fas fa-calendar"></i> ${formatDate(plugin.date)}</span>
                </div>
                <button class="download-btn" onclick="downloadPlugin(event, ${plugin.id})">
                    <i class="fas fa-download"></i>
                    Download
                </button>
            </div>
        </div>
    `).join('');
}

// Setup event listeners
function setupEventListeners() {
    // Search functionality
    searchInput.addEventListener('input', handleSearch);
    
    // Filter functionality
    categoryFilter.addEventListener('change', handleFilters);
    sortFilter.addEventListener('change', handleFilters);
    
    // Category cards click
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', function() {
            const category = this.dataset.category;
            categoryFilter.value = category;
            handleFilters();
            scrollToSection('plugins');
        });
    });
    
    // Upload form
    uploadForm.addEventListener('submit', handleUpload);
    
    // File drop zone
    setupFileUpload();
    
    // Modal
    setupModal();
}

// Setup navigation
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
            
            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Search and filter functions
function handleSearch() {
    const searchTerm = searchInput.value.toLowerCase();
    const filteredPlugins = plugins.filter(plugin => 
        plugin.name.toLowerCase().includes(searchTerm) ||
        plugin.description.toLowerCase().includes(searchTerm) ||
        plugin.author.toLowerCase().includes(searchTerm) ||
        plugin.tags.some(tag => tag.toLowerCase().includes(searchTerm))
    );
    
    applyFiltersAndSort(filteredPlugins);
}

function handleFilters() {
    let filteredPlugins = [...plugins];
    
    // Apply search filter
    const searchTerm = searchInput.value.toLowerCase();
    if (searchTerm) {
        filteredPlugins = filteredPlugins.filter(plugin => 
            plugin.name.toLowerCase().includes(searchTerm) ||
            plugin.description.toLowerCase().includes(searchTerm) ||
            plugin.author.toLowerCase().includes(searchTerm) ||
            plugin.tags.some(tag => tag.toLowerCase().includes(searchTerm))
        );
    }
    
    // Apply category filter
    const selectedCategory = categoryFilter.value;
    if (selectedCategory) {
        filteredPlugins = filteredPlugins.filter(plugin => plugin.category === selectedCategory);
    }
    
    applyFiltersAndSort(filteredPlugins);
}

function applyFiltersAndSort(filteredPlugins) {
    // Apply sorting
    const sortBy = sortFilter.value;
    
    switch (sortBy) {
        case 'newest':
            filteredPlugins.sort((a, b) => new Date(b.date) - new Date(a.date));
            break;
        case 'popular':
            filteredPlugins.sort((a, b) => b.rating - a.rating);
            break;
        case 'downloads':
            filteredPlugins.sort((a, b) => b.downloads - a.downloads);
            break;
    }
    
    renderPlugins(filteredPlugins);
}

// File upload functionality
function setupFileUpload() {
    // Drag and drop
    fileDropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = '#2a5298';
        this.style.background = '#f0f8ff';
    });
    
    fileDropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.borderColor = '#ccc';
        this.style.background = 'transparent';
    });
    
    fileDropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.borderColor = '#ccc';
        this.style.background = 'transparent';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            pluginFile.files = files;
            showFilePreview(files[0]);
        }
    });
    
    // File input change
    pluginFile.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            showFilePreview(e.target.files[0]);
        }
    });
}

function showFilePreview(file) {
    const preview = document.getElementById('filePreview');
    preview.style.display = 'block';
    
    const fileInfo = `
        <div style="display: flex; align-items: center; gap: 1rem;">
            <i class="fas fa-file-code" style="font-size: 2rem; color: #2a5298;"></i>
            <div>
                <h4>${file.name}</h4>
                <p>Tamanho: ${(file.size / 1024).toFixed(2)} KB</p>
                <p>Tipo: ${file.type || 'Arquivo de plugin'}</p>
            </div>
        </div>
    `;
    
    preview.innerHTML = fileInfo;
}

// Upload form handler
function handleUpload(e) {
    e.preventDefault();
    
    // Get form data
    const formData = {
        name: document.getElementById('pluginName').value,
        author: document.getElementById('pluginAuthor').value,
        category: document.getElementById('pluginCategory').value,
        description: document.getElementById('pluginDescription').value,
        tags: document.getElementById('pluginTags').value.split(',').map(tag => tag.trim()),
        version: document.getElementById('pluginVersion').value,
        file: pluginFile.files[0]
    };
    
    // Validate
    if (!formData.file) {
        showMessage('Por favor, selecione um arquivo para upload.', 'error');
        return;
    }
    
    // Simulate upload
    showMessage('Enviando plugin...', 'info');
    
    setTimeout(() => {
        // Add to plugins array
        const newPlugin = {
            id: plugins.length + 1,
            name: formData.name,
            author: formData.author,
            category: formData.category,
            description: formData.description,
            tags: formData.tags,
            version: formData.version,
            downloads: 0,
            rating: 0,
            date: new Date().toISOString().split('T')[0],
            fileSize: Math.round(formData.file.size / 1024) + ' KB'
        };
        
        plugins.unshift(newPlugin);
        updateStats();
        renderPlugins(plugins);
        
        showMessage('Plugin enviado com sucesso!', 'success');
        uploadForm.reset();
        filePreview.style.display = 'none';
        
        // Scroll to plugins section
        setTimeout(() => {
            scrollToSection('plugins');
        }, 1000);
    }, 2000);
}

// Modal functionality
function setupModal() {
    const closeBtn = document.querySelector('.close');
    
    closeBtn.addEventListener('click', closeModal);
    
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
}

function openPluginModal(pluginId) {
    const plugin = plugins.find(p => p.id === pluginId);
    if (!plugin) return;
    
    const modalHTML = `
        <h2>${plugin.name}</h2>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="color: #666;">por ${plugin.author}</span>
            <span class="plugin-category" style="background: #2a5298; color: white; padding: 0.25rem 0.75rem; border-radius: 15px;">
                ${getCategoryName(plugin.category)}
            </span>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
            <div>
                <h4>Informações</h4>
                <ul style="list-style: none; padding: 0;">
                    <li><strong>Versão:</strong> ${plugin.version}</li>
                    <li><strong>Downloads:</strong> ${plugin.downloads.toLocaleString()}</li>
                    <li><strong>Avaliação:</strong> ${plugin.rating}/5 ⭐</li>
                    <li><strong>Tamanho:</strong> ${plugin.fileSize}</li>
                    <li><strong>Data:</strong> ${formatDate(plugin.date)}</li>
                </ul>
            </div>
            <div>
                <h4>Tags</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    ${plugin.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        </div>
        
        <h4>Descrição</h4>
        <p style="line-height: 1.6; margin-bottom: 2rem;">${plugin.description}</p>
        
        <div style="text-align: center;">
            <button class="download-btn" onclick="downloadPlugin(event, ${plugin.id})" style="font-size: 1.1rem; padding: 1rem 2rem;">
                <i class="fas fa-download"></i>
                Download Plugin
            </button>
        </div>
    `;
    
    modalContent.innerHTML = modalHTML;
    modal.style.display = 'block';
}

function closeModal() {
    modal.style.display = 'none';
}

// Download functionality
function downloadPlugin(event, pluginId) {
    event.stopPropagation();
    
    const plugin = plugins.find(p => p.id === pluginId);
    if (!plugin) return;
    
    // Increment download count
    plugin.downloads++;
    updateStats();
    
    // Update the display
    if (event.target.closest('.plugin-card')) {
        renderPlugins(getFilteredPlugins());
    }
    
    // Simulate download
    showMessage(`Baixando ${plugin.name}...`, 'info');
    
    // In a real application, this would trigger an actual file download
    setTimeout(() => {
        showMessage(`${plugin.name} baixado com sucesso!`, 'success');
    }, 1500);
}

// Utility functions
function getCategoryName(category) {
    const categories = {
        'admin': 'Admin Tools',
        'gameplay': 'Gameplay',
        'weapons': 'Armas',
        'hud': 'HUD/Interface',
        'maps': 'Mapas',
        'fun': 'Diversão'
    };
    return categories[category] || category;
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
}

function getFilteredPlugins() {
    let filteredPlugins = [...plugins];
    
    // Apply search filter
    const searchTerm = searchInput.value.toLowerCase();
    if (searchTerm) {
        filteredPlugins = filteredPlugins.filter(plugin => 
            plugin.name.toLowerCase().includes(searchTerm) ||
            plugin.description.toLowerCase().includes(searchTerm) ||
            plugin.author.toLowerCase().includes(searchTerm) ||
            plugin.tags.some(tag => tag.toLowerCase().includes(searchTerm))
        );
    }
    
    // Apply category filter
    const selectedCategory = categoryFilter.value;
    if (selectedCategory) {
        filteredPlugins = filteredPlugins.filter(plugin => plugin.category === selectedCategory);
    }
    
    // Apply sorting
    const sortBy = sortFilter.value;
    switch (sortBy) {
        case 'newest':
            filteredPlugins.sort((a, b) => new Date(b.date) - new Date(a.date));
            break;
        case 'popular':
            filteredPlugins.sort((a, b) => b.rating - a.rating);
            break;
        case 'downloads':
            filteredPlugins.sort((a, b) => b.downloads - a.downloads);
            break;
    }
    
    return filteredPlugins;
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const navHeight = document.querySelector('.navbar').offsetHeight;
        const sectionTop = section.offsetTop - navHeight - 20;
        
        window.scrollTo({
            top: sectionTop,
            behavior: 'smooth'
        });
    }
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.success-message, .error-message, .info-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `${type}-message`;
    messageDiv.textContent = message;
    
    // Add to upload form
    const uploadContainer = document.querySelector('.upload-container');
    uploadContainer.insertBefore(messageDiv, uploadContainer.querySelector('.upload-form'));
    
    // Remove after 3 seconds for success/error messages
    if (type !== 'info') {
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}

// Smooth scrolling for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const navHeight = document.querySelector('.navbar').offsetHeight;
            const targetTop = target.offsetTop - navHeight - 20;
            
            window.scrollTo({
                top: targetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Active navigation highlighting on scroll
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        const navHeight = document.querySelector('.navbar').offsetHeight;
        
        if (window.pageYOffset >= sectionTop - navHeight - 100) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});