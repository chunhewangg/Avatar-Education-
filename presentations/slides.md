---
theme: none
background: '#ffffff'
class: text-center
highlighter: shiki
lineNumbers: false
colorSchema: light
info: |
  ## AI Avatar Workshop
  Complete 5-Class Course for High School Students
drawings:
  persist: false
transition: slide-left
title: AI Avatar Workshop
mdc: true
css: unocss
---

<style>
/* AI Tech Theme - Light Mode */
:root {
  --slidev-theme-primary: #3b82f6;
  --slidev-theme-secondary: #8b5cf6;
  --slidev-theme-accent: #06b6d4;
  --slidev-theme-neutral: #1f2937;
  --slidev-code-background: #f8fafc;
  --slidev-code-foreground: #374151;
}

.slidev-layout {
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f0f9ff 100%);
  font-family: 'Inter', 'SF Pro Display', system-ui, sans-serif;
  color: #1f2937;
}

/* Headers with tech gradient */
h1 {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  font-size: 3rem !important;
  margin-bottom: 1rem;
}

h2 {
  color: #374151;
  font-weight: 700;
  font-size: 2rem !important;
  margin-bottom: 0.75rem;
}

h3 {
  color: #4b5563;
  font-weight: 600;
  font-size: 1.5rem !important;
  margin-bottom: 0.5rem;
}

/* Tech-style buttons */
button {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  padding: 1rem 2rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
}

/* Tech card styles */
.tech-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.tech-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  border-color: rgba(59, 130, 246, 0.4);
}

/* AI-style gradients */
.ai-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px;
  padding: 2rem;
}

.tech-gradient {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border-radius: 16px;
  padding: 2rem;
}

.cyber-gradient {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border-radius: 16px;
  padding: 2rem;
}

/* Code blocks with AI theme */
.slidev-code {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

/* Links with tech styling */
a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

a:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

/* Success/celebration styles */
.success-card {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
}

/* Warning/challenge styles */
.challenge-card {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3);
}

/* Section backgrounds */
.section-bg-1 { background: linear-gradient(135deg, #e0e7ff 0%, #f0f9ff 100%); }
.section-bg-2 { background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%); }
.section-bg-3 { background: linear-gradient(135deg, #fef3c7 0%, #fef7cd 100%); }
.section-bg-4 { background: linear-gradient(135deg, #fce7f3 0%, #fdf2f8 100%); }
.section-bg-5 { background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%); }

/* Tech grid styling */
.tech-grid {
  display: grid;
  gap: 1.5rem;
  margin: 2rem 0;
}

/* Ensure light theme throughout */
.dark .slidev-layout,
.dark h1,
.dark h2, 
.dark h3,
.dark p {
  color: #1f2937 !important;
  background: transparent !important;
}

/* Override any dark theme defaults */
html.dark {
  color-scheme: light !important;
}

.slidev-layout.dark {
  background: linear-gradient(135deg, #f8fafc 0%, #ffffff 50%, #f0f9ff 100%) !important;
  color: #1f2937 !important;
}
</style>

# 🤖 AI Avatar Workshop
## Build Your Own Talking Avatar App!

Welcome to the most exciting AI course ever!

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space to start <carbon:arrow-right class="inline"/>
  </span>
</div>

---
layout: center
class: text-center
---

# Choose Your Class

<div class="grid grid-cols-1 gap-4 max-w-md mx-auto">
  <button @click="$slidev.nav.go(3)" class="bg-blue-500 text-white px-6 py-4 rounded-lg hover:bg-blue-600 transition-colors">
    🧠 Class 1: AI Foundations & Python
  </button>
  <button @click="$slidev.nav.go(12)" class="bg-green-500 text-white px-6 py-4 rounded-lg hover:bg-green-600 transition-colors">
    🌐 Class 2: Web Apps & APIs
  </button>
  <button @click="$slidev.nav.go(21)" class="bg-purple-500 text-white px-6 py-4 rounded-lg hover:bg-purple-600 transition-colors">
    🎭 Class 3: Avatar Technology
  </button>
  <button @click="$slidev.nav.go(30)" class="bg-orange-500 text-white px-6 py-4 rounded-lg hover:bg-orange-600 transition-colors">
    ⚡ Class 4: Integration & Features
  </button>
  <button @click="$slidev.nav.go(39)" class="bg-red-500 text-white px-6 py-4 rounded-lg hover:bg-red-600 transition-colors">
    🏆 Class 5: Demo Day & Projects
  </button>
</div>

---
layout: section
background: '#ddd6fe'
---

# 🧠 Class 1
## AI Foundations & Python Power

---

# 🎯 What We'll Build Together

<div class="grid grid-cols-3 gap-8 py-8">
  <div class="text-center">
    <div class="text-6xl mb-4">💬</div>
    <div class="text-xl font-bold">Chat with AI</div>
  </div>
  <div class="text-center">
    <div class="text-6xl mb-4">🎭</div>
    <div class="text-xl font-bold">Generate Avatar</div>
  </div>
  <div class="text-center">
    <div class="text-6xl mb-4">🎬</div>
    <div class="text-xl font-bold">Talking Videos</div>
  </div>
</div>

**Final Product**: Your personalized AI assistant with a realistic human face!

---

# 🚀 Your 5-Week Journey

<div class="ai-gradient">

**Week 1:** 🧠 AI Foundations + Python  
**Week 2:** 🌐 Web Apps + APIs  
**Week 3:** 🎭 Avatar Technology  
**Week 4:** ⚡ Integration Magic  
**Week 5:** 🏆 Group Projects & Demo  

</div>  

---

# 🤯 Try AI Magic NOW!

### 🔥 Live Demos
- **🤖 [Chat with Claude](https://claude.ai)** - See what we're building with!
- **🎭 [HeyGen Avatars](https://app.heygen.com/guest/avatar)** - Mind-blowing realistic avatars
- **🐍 [Google Colab](https://colab.research.google.com)** - Python in your browser
- **🚀 [Streamlit Cloud](https://streamlit.io)** - Deploy apps instantly

---

# 🎮 Today's Mission

## 🎯 Hour 1: Decode AI Magic
- 🤖 AI Evolution: Calculators → ChatGPT
- 🧠 Attention Mechanism & Transformers
- 🎭 Avatar Science Basics

## 🎯 Hour 2: Python Superpowers
- ⚙️ Environment Setup
- 🐍 Python Essentials
- 💬 Build Your First Chatbot

---

# 🎪 Interactive Demo Time!

## Let's Break the Internet! 🌐

**Live Demo Stations** (5 min each group):

🔹 **Station 1:** Chat with Claude AI  
🔹 **Station 2:** Generate AI avatars  
🔹 **Station 3:** Python coding playground  
🔹 **Station 4:** Streamlit app showcase  

### 🏁 Ready to become AI wizards?

---

# 🎓 Success Checklist

## By the end of today, you'll have:

✅ **Understanding** of how modern AI actually works  
✅ **Python environment** set up and running  
✅ **First chatbot** built and working  
✅ **Mind blown** by avatar technology demos  
✅ **Excitement** for building your own AI app  

### 🚀 Next Week: We build web apps that the world can use!

---
layout: section
background: '#dcfce7'
---

# 🌐 Class 2
## Web Apps & API Magic

---

# Today's Epic Mission

## 🚀 Build Web Apps
With Streamlit magic

## 🔌 Connect APIs
Talk to Claude AI

## 💬 Create Chat UI
Interactive & beautiful

**Goal:** Your chat app goes from localhost to the internet!

---

# 🎮 Hour 1: Streamlit Superpowers

## 🌟 Why Streamlit Rocks
- **⚡ Zero HTML/CSS needed** - Pure Python magic
- **🔄 Live reload** - See changes instantly
- **📱 Mobile ready** - Works everywhere
- **☁️ Easy deploy** - Share with the world

## 🛠️ What We'll Build
- **Sidebar controls** for user preferences
- **Chat history display** with styling
- **Input forms** for user messages
- **Progress indicators** for loading states

---

# 🔥 Live Coding Session!

## Follow Along Stations (Everyone codes together!)

**🎨 Station 1: UI Elements** - Buttons, sliders, text inputs  
**💾 Station 2: State Management** - Remember user data  
**🎭 Station 3: Layout Magic** - Columns, containers, sidebars  
**📊 Station 4: Data Display** - Charts, tables, media  

---

# 🔌 Hour 2: API Adventures

## 🎯 API Mastery Checklist

### ✅ Understanding APIs
What's an API? RESTful architecture, Authentication with API keys

### ✅ Python Requests Library
Making HTTP calls, handling responses and errors, async programming

### ✅ Claude API Integration
Setting up Anthropic client, crafting prompts, processing AI responses

---

# 🎪 Hands-On Challenge Time!

## 🏆 Build Your Chat Interface
*30 minutes collaborative coding!*

<div class="challenge-card">

### Challenge Levels:

**🥉 Beginner** - Basic chat with Claude  
**🥈 Intermediate** - Styled chat history  
**🥇 Advanced** - Full-featured chat  

</div>  

---

# 🌐 Deployment Magic!

## From Local to Global in 3 Steps

**Step 1:** Push to GitHub 📤  
**Step 2:** Connect Streamlit Cloud ☁️  
**Step 3:** Share your URL with friends! 🔗  

### 🎉 Your app is now LIVE on the internet!

**Try it now:** [Streamlit Cloud](https://streamlit.io/cloud) - Free hosting!

---

# 🏆 Success Celebration!

<div class="success-card">

## What You've Accomplished Today:

✅ **Built a real web application** that runs in browsers  
✅ **Connected to AI services** through APIs  
✅ **Created interactive chat interfaces** with styling  
✅ **Deployed to the cloud** - your app is public!  
✅ **Mastered modern web development** workflow  

</div>  

### 🚀 Next Week: Avatar Generation Deep Dive!
*We'll make our chatbot speak with realistic human faces*

---
layout: section
background: '#fef3c7'
---

# 🎭 Class 3
## Avatar Technology Deep Dive

---

# Welcome to the Future!

## ✨ Today We Decode the Magic

### 🧠 Neural Networks
How AI creates faces

### 🎨 Diffusion Models
From noise to photorealism

### 🎬 Video Generation
Making avatars talk & move

---

# 🔬 The Science Behind Digital Humans

## 🎨 Diffusion Models
- Start with random noise
- Gradually remove noise
- Reveal photorealistic images
- **Like sculpting from chaos!**

## 🧠 Neural Rendering
- 3D face understanding
- Lighting & texture mapping
- Real-time ray tracing
- **Digital cinematography!**

---

# 🎪 Interactive Tech Demos!

## See the Magic Happen Live! 🎬

**🎭 Station 1: Avatar Playground** - [HeyGen Studio](https://app.heygen.com/studio)  
**🎨 Station 2: Diffusion Visualization** - [Stable Diffusion Demo](https://huggingface.co/spaces/stabilityai/stable-diffusion)  
**🧠 Station 3: Neural Network Explorer** - [TensorFlow Playground](https://playground.tensorflow.org)  
**🎬 Station 4: 3D Face Technology** - [Face Mesh Demo](https://codepen.io/mediapipe/pen/OJWVGbZ)  

---

# 💻 Build Your Avatar Generator!

## 🏆 Team Coding Session
*45 minutes of avatar magic!*

**🌱 Starter Mission** - Connect to avatar API, send basic text request, display generated video  
**🚀 Power User** - Multiple avatar selection, progress indicators, error handling  
**🎯 Avatar Master** - Custom styling options, batch processing, advanced animations  

**Bonus Challenge:** Create avatars that speak different languages! 🌍

---

# 🎉 Avatar Creation Celebration!

## What You've Mastered Today:

✅ **Deep understanding** of avatar generation technology  
✅ **Hands-on experience** with cutting-edge AI APIs  
✅ **Working avatar generator** integrated into your app  
✅ **Performance optimization** techniques  
✅ **Ethical AI awareness** and best practices  

### 🚀 Next Week Preview:
*We combine everything into one epic app!*

---
layout: section
background: '#fce7f3'
---

# ⚡ Class 4
## Integration & Advanced Features

---

# The Grand Assembly!

## 🚀 Today: Your App Becomes EPIC

### 🔗 Connect Everything
Chat + Avatar = Magic

### 🎨 Polish UI/UX
Make it beautiful

### 🛡️ Add Superpowers
Advanced features

---

# 🏗️ Integration Architecture

```
User Input → Claude AI → Avatar Generation → Video Display → User Interaction
↑                                                              ↓
←←←←←←←←←←← Conversation Memory ←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

## 🔧 Integration Checklist

**⚡ Data Flow** - Message routing, state synchronization, error propagation, loading states  
**🎨 User Experience** - Seamless interactions, progress indicators, responsive design, accessibility  

---

# 🎨 Advanced Features Menu

## 🧠 Smart Memory
- Conversation context
- User preferences
- Learning from interactions
- **Make AI remember everything!**

## 🎭 Avatar Personalities
- Different character modes
- Voice & style variations
- Emotional expressions
- **Multiple AI personalities!**

---

# 💻 Ultimate Coding Challenge!

## 🏆 Build Your Dream App
*60 minutes of pure coding power!*

**🎯 Mission: Possible** - Complete integration working, basic error handling, clean UI  
**🚀 Mission: Awesome** - Advanced features added, professional styling, performance optimized  
**🎭 Mission: Legendary** - Multiple personalities, custom animations, innovative features  

**Team Support Available:** Coding mentors at each table! 👨‍💻👩‍💻

---

# 🎉 Integration Victory!

## You've Achieved the Impossible:

✅ **Complete AI Avatar Chat App** working end-to-end  
✅ **Advanced features** that wow users  
✅ **Professional code quality** with error handling  
✅ **Beautiful user interface** with smooth interactions  
✅ **Deep understanding** of complex system integration  

### 🎊 You're Now Full-Stack AI Developers!

### 🚀 Next Week: The Grand Finale!
*Group projects, team collaboration, and epic demonstrations*  
**Get ready to blow minds! 🤯**

---
layout: section
background: '#fee2e2'
---

# 🏆 Class 5
## Group Projects & Demo Day

---

# Welcome to Demo Day!

## 🎉 Today You Become AI Legends!

### 👥 Team Up
Form epic groups of 3

### 🚀 Build Together
Combine your superpowers

### 🎭 Present
Blow everyone's minds

**Goal:** Create the most amazing AI Avatar app the world has ever seen! 🌟

---

# 👥 The Dream Team Assembly

## 🎨 UI/UX Designer
Makes it beautiful
- Visual design
- User experience
- Animations & styling

## ⚡ Backend Engineer
Makes it work
- API integration
- Data management
- Performance optimization

## 🎤 Presentation Lead
Makes it shine
- Demo planning
- Storytelling
- Audience engagement

---

# 🚀 Choose Your Adventure

**🎭 Avatar Personality Creator** - Different AI characters  
**🌍 Multilingual Avatar Teacher** - Learn languages with AI  
**🎮 Interactive Avatar Game** - Gamified conversations  
**🧠 Study Buddy Avatar** - AI homework helper  
**🎪 Entertainment Avatar** - Jokes, stories, fun!  
**💡 Custom Concept** - Your wild creative idea!  

---

# 💻 The Ultimate Coding Sprint!

## ⚡ 45 Minutes of Pure Creation

### Sprint Goals - Pick Your Level:

**🥉 MVP Master** - Working group app, unified design theme, one unique feature  
**🥈 Feature Champion** - Multiple unique features, professional polish, great UX  
**🥇 Innovation Legend** - Revolutionary concept, multiple personalities, mind-blowing demo  

**Mentorship Available:** Instructors rotating between teams! 🧑‍🏫

---

# 🎬 The Perfect Demo

## 🎯 6-Minute Demo Format

**🎬 Minute 1:** Hook - show coolest feature first!  
**💡 Minute 2:** Explain concept & why it's amazing  
**⚡ Minute 3:** Live demo - let app speak for itself  
**🔧 Minute 4:** Technical challenges & solutions  
**👥 Minute 5:** Each team member's contribution  
**🚀 Minute 6:** Future vision & Q&A  

### Demo Success Tips:
- **Test everything twice** - Murphy's law loves live demos!
- **Have backup plans** - Screenshots for tech issues
- **Practice transitions** - Smooth team handoffs
- **Engage audience** - Ask questions, get reactions!

---

# 🎪 The Grand Showcase!

## 🌟 Epic Presentations

### 🎭 Team Presentations (45 min)
- Live app demonstrations
- Technical deep-dives
- Creative feature showcases
- Problem-solving stories

### 🗳️ Peer Voting (15 min)
- Most Creative Concept 🎨
- Best Technical Implementation ⚡
- Outstanding User Experience 🌟
- Most Realistic Avatar 🎭
- Audience Choice Award 🏆

---

# 🏆 Victory Celebration!

## What You've Accomplished is INCREDIBLE:

✅ **Built complete AI Avatar application** from scratch  
✅ **Mastered cutting-edge AI technologies** in 5 weeks  
✅ **Collaborated on complex projects** like professional developers  
✅ **Presented technical work** with confidence  
✅ **Created something that didn't exist** before this course  

### 🎊 You Are Now AI Developers! 🎊

---

# 🚀 Your Journey Continues...

## 🎓 Next Steps:
- Keep building with premium avatar platform access
- Join our developer community Discord
- Explore advanced AI/ML courses
- Consider computer science programs
- Share projects on social media!

### 💡 You've just scratched the surface of what's possible!

---

# 🌟 Final Inspiration

## The Future is What You Build ✨

### You've learned to create AI that can:
🧠 Think and reason like humans  
💬 Communicate naturally  
🎭 Express with realistic avatars  
🌐 Reach anyone, anywhere  

## The next AI breakthrough might come from YOU!

### 🎯 Keep building. Keep dreaming. Keep pushing boundaries.

---
layout: end
---

# Thank You! 🙏

## You've Been Amazing! 🌟

Questions? Feedback? Let's connect!

Remember: The best way to predict the future is to build it! 🚀