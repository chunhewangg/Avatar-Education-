# 🤖 AI Avatar Education Workshop

Complete 5-class workshop for high school students to build AI Avatar chat applications.

## 📋 Table of Contents

- [Workshop Overview](#workshop-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Presentation](#running-the-presentation)
- [Workshop Structure](#workshop-structure)
- [Troubleshooting](#troubleshooting)

## 🎯 Workshop Overview

This workshop teaches high school students to build AI-powered avatar chat applications through 5 progressive classes:

1. **AI Foundations & Python** - Understanding AI and Python basics
2. **Web Apps & APIs** - Building web interfaces with Streamlit
3. **Avatar Technology** - Deep dive into digital human creation
4. **Integration & Features** - Combining all components
5. **Group Projects & Demo Day** - Team collaboration and presentations

## 📚 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11 with WSL2, macOS, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: Stable connection for downloads and API calls

### Knowledge Requirements
- Basic computer literacy
- No prior programming experience required
- Enthusiasm for AI and technology!

## 🚀 Installation

### Step 1: Install Node.js (WSL2/Linux/macOS)

**For WSL2 (Windows Subsystem for Linux):**

```bash
# Update package list
sudo apt update

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

**For macOS:**
```bash
# Using Homebrew (install Homebrew first if needed)
brew install node

# Or download from https://nodejs.org/
```

**For Windows (if not using WSL2):**
- Download from [nodejs.org](https://nodejs.org/)
- Run the installer and follow instructions

### Step 2: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/your-username/Avatar-Education-.git

# Navigate to the project
cd Avatar-Education-
```

### Step 3: Install Presentation Dependencies

```bash
# Navigate to presentations folder
cd presentations

# Install Slidev and dependencies
npm install

# Verify installation
npx slidev --version
```

## 🎪 Running the Presentation

### Start the Presentation Server

```bash
# Make sure you're in the presentations folder
cd presentations

# Start Slidev development server
npm run dev

# Alternative method
npx slidev slides.md
```

### Access the Presentation

1. **Open your browser** and go to: `http://localhost:3030`
2. **Use the navigation menu** to jump to any class
3. **Navigate with:**
   - **Arrow keys** - Move between slides
   - **Space bar** - Next slide
   - **Escape** - Exit fullscreen

### Presentation Controls

| Key | Action |
|-----|--------|
| `→` / `Space` | Next slide |
| `←` | Previous slide |
| `↑` / `↓` | Navigate vertical slides |
| `F` | Toggle fullscreen |
| `O` | Overview mode |
| `P` | Presenter mode |
| `D` | Drawing mode |
| `Esc` | Exit modes |

### Stop the Server

```bash
# Press Ctrl+C in the terminal to stop the server
```

## 📖 Workshop Structure

### 🧠 Class 1: AI Foundations & Python Power
- **Duration**: 2.5 hours
- **Focus**: Understanding AI, Python basics, first chatbot
- **Navigation**: Click "Class 1" button or go to slide 3

### 🌐 Class 2: Web Apps & API Magic  
- **Duration**: 2.5 hours
- **Focus**: Streamlit web apps, API integration
- **Navigation**: Click "Class 2" button or go to slide 12

### 🎭 Class 3: Avatar Technology Deep Dive
- **Duration**: 2.5 hours  
- **Focus**: Digital humans, avatar generation APIs
- **Navigation**: Click "Class 3" button or go to slide 21

### ⚡ Class 4: Integration & Advanced Features
- **Duration**: 2.5 hours
- **Focus**: Combining components, advanced features
- **Navigation**: Click "Class 4" button or go to slide 30

### 🏆 Class 5: Group Projects & Demo Day
- **Duration**: 2.5 hours
- **Focus**: Team projects, presentations, celebration
- **Navigation**: Click "Class 5" button or go to slide 39

## 🛠 Troubleshooting

### Common Issues

#### "npm: command not found"
```bash
# Reinstall Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### "Permission denied" errors (WSL2)
```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
```

#### Port 3030 already in use
```bash
# Kill process using port 3030
sudo lsof -t -i tcp:3030 | xargs kill -9

# Or use different port
npx slidev slides.md --port 3031
```

#### Presentation looks broken
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules
npm install
```

#### WSL2 can't access localhost
- Use `http://localhost:3030` in browser
- If that fails, try `http://127.0.0.1:3030`
- Or find WSL2 IP: `ip addr show eth0`

#### Slides not updating
- **Hard refresh**: `Ctrl+F5` or `Cmd+Shift+R`
- **Clear browser cache**
- **Restart Slidev server**: `Ctrl+C` then `npm run dev`

### Performance Tips

1. **Close other applications** to free up RAM
2. **Use Chrome/Firefox** for best compatibility  
3. **Close unnecessary browser tabs**
4. **Restart computer** if experiencing slowness

### Getting Help

1. **Check the terminal** for error messages
2. **Restart the presentation server**
3. **Try a different browser**
4. **Ask your instructor** for assistance

## 📁 Project Structure

```
Avatar-Education-/
├── README.md                 # This file
├── presentations/           # Slidev presentation
│   ├── slides.md           # Main presentation file
│   ├── package.json        # Dependencies
│   ├── .gitignore         # Git ignore rules
│   └── node_modules/      # Installed packages (ignored by git)
├── avatar_generation.py    # Python avatar generation script
├── chat_multilingual.py   # Multilingual chat script
└── *.pdf                  # Course materials
```

## 🔧 Advanced Usage

### Exporting Presentations

```bash
# Export to PDF
npm run export

# Export specific slides
npx slidev export slides.md --format pdf

# Export as images
npx slidev export slides.md --format png
```

### Development Mode

```bash
# Run with auto-reload
npm run dev

# Run on specific port
npx slidev slides.md --port 8080

# Run with remote access
npx slidev slides.md --host 0.0.0.0
```

## 📝 Notes for Instructors

- **Test setup** before class starts
- **Have backup slides** as PDFs in case of technical issues
- **Encourage interaction** during demo stations
- **Take screenshots** of student projects for celebration
- **Prepare API keys** in advance for students

## 🎉 Have Fun!

This workshop is designed to be exciting and hands-on. Encourage students to:
- **Ask questions** throughout
- **Experiment** with the technology
- **Collaborate** and help each other
- **Share their creations** with pride
- **Dream big** about AI's future

---

**Questions?** Open an issue or contact the workshop instructors!

**Happy Coding!** 🚀