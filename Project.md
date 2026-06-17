# AI MARKETING OPERATING SYSTEM

## Project Overview

Build an enterprise-grade AI Marketing Operating System for an AI Consultancy.

The system must autonomously:

* Research markets
* Analyze competitors
* Discover customer pain points
* Generate campaign strategies
* Create platform-specific content
* Generate videos
* Generate images
* Generate carousels
* Maintain brand consistency
* Publish content
* Collect analytics
* Learn from performance
* Improve future content

The system must be modular, scalable, secure, and production-ready.

---

# Primary Goal

Input:

* Product Information
* AI Tool Information
* AI Agent Information
* Service Information
* Target Audience
* Campaign Goal

Output:

* Professional Marketing Assets
* Videos
* Carousels
* Images
* Social Posts
* Publishing Schedule
* Analytics
* Learnings
* Optimized Future Campaigns

---

# Architecture

Frontend:

* Vue 3
* Nuxt 3
* TailwindCSS
* ECharts

Backend:

* FastAPI

Agent Framework:

* LangGraph

Database:

* PostgreSQL

Cache:

* Redis

Background Jobs:

* Celery

Storage:

* Cloudflare R2

Monitoring:

* Grafana

Deployment:

* Railway (MVP)
* AWS (Production)

---

# Core LangGraph State

```python
class CampaignState(TypedDict):

    campaign: dict

    research: dict

    platform_rules: dict

    strategy: dict

    content_plan: dict

    content_format: dict

    story: dict

    assets: dict

    quality: dict

    analytics: dict

    learnings: dict

    optimization: dict
```

Every agent reads from and updates this shared state.

No agent should communicate directly with another agent.

---

# Agent 1: Research Agent

Goal:
Research market before creating content.

Responsibilities:

* Competitor Analysis
* Reddit Analysis
* Pain Point Discovery
* Trend Discovery
* Customer Desire Discovery

Tools:

Paid:

* GPT-5
* Perplexity API
* Firecrawl

Free:

* DeepSeek
* Crawl4AI

Output:

research

---

# Agent 2: Platform Intelligence Agent

Goal:
Monitor platform requirements continuously.

Platforms:

* LinkedIn
* Instagram
* Facebook
* X
* YouTube
* Pinterest

Store:

* Video Length Limits
* Image Sizes
* Carousel Limits
* Caption Limits
* API Requirements

Run daily.

Output:

platform_rules

---

# Agent 3: Strategy Agent

Goal:
Act as a marketing strategist.

Determine:

* Campaign Theme
* Positioning
* Core Emotion
* Marketing Angle
* Offer Strategy

Tools:

Paid:

* GPT-5
* Claude

Free:

* DeepSeek
* Qwen

Output:

strategy

---

# Agent 4: Content Planner Agent

Goal:
Generate a 30-day content calendar.

Generate:

* Founder Stories
* Case Studies
* AI Demos
* Product Breakdowns
* Educational Content
* Behind-the-Scenes Content

Output:

content_plan

---

# Agent 5: Creative Director Agent

Goal:
Choose optimal content format.

Possible Formats:

* Video
* Carousel
* Image
* Thread
* Short Video
* Long Video
* Founder Story
* Case Study

Per platform determine:

* Content Type
* Duration
* Layout
* CTA

Output:

content_format

---

# Agent 6: Storytelling Agent

Goal:
Create high-converting content.

Generate:

* Hooks
* Scripts
* Narratives
* CTAs
* Scene Descriptions

Frameworks:

* AIDA
* PAS
* StoryBrand
* Hero Journey

Output:

story

---

# Agent 7: Image Agent

Goal:
Generate professional images.

Tools:

Paid:

* Midjourney
* Ideogram

Free:

* Flux
* Stable Diffusion

Generate:

* Ads
* Thumbnails
* Social Graphics
* Banners

Output:

assets.images

---

# Agent 8: Carousel Agent

Goal:
Generate carousels.

Tools:

Paid:

* Canva API
* Figma API

Free:

* PPTX Templates

Generate:

* LinkedIn Carousels
* Instagram Carousels

Output:

assets.carousels

---

# Agent 9: Video Agent

Goal:
Generate marketing videos.

UGC Video Tools:

* Creatify
* Arcads

Video Tools:

* Runway
* Luma

Free:

* ComfyUI
* Open Source Video Models

Generate:

* Product Videos
* Explainer Videos
* Founder Videos
* Demo Videos

Output:

assets.video_scenes

---

# Agent 10: Voice Agent

Goal:
Generate voiceovers.

Paid:

* ElevenLabs

Free:

* Piper
* Coqui

Output:

assets.voice

---

# Agent 11: Video Editor Agent

Goal:
Produce final video.

Primary Tool:

* Remotion

Fallback:

* FFmpeg

Responsibilities:

* Captions
* Branding
* Animations
* Music
* Transitions

Output:

assets.final_video

---

# Agent 12: Brand Guardian Agent

Goal:
Enforce brand consistency.

Validate:

* Colors
* Fonts
* Logos
* Tone
* Voice

Reject assets violating brand rules.

Output:

quality.brand_score

---

# Agent 13: Quality Control Agent

Goal:
Ensure professional quality.

Validate:

* Grammar
* Visual Quality
* Readability
* CTA Quality
* Professional Appearance

Output:

quality.review

---

# Agent 14: Publisher Agent

Goal:
Publish assets.

Platforms:

* LinkedIn
* Instagram
* Facebook
* X
* YouTube
* Pinterest

Validate:

* Dimensions
* Length
* Caption Limits
* API Requirements

Output:

publication_records

---

# Agent 15: Analytics Agent

Goal:
Collect performance metrics.

Track:

* Views
* Reach
* CTR
* Watch Time
* Shares
* Comments
* Leads
* Revenue

Output:

analytics

---

# Agent 16: Learning Agent

Goal:
Discover winning patterns.

Determine:

* Best Hooks
* Best Video Lengths
* Best CTA
* Best Formats
* Best Posting Times

Store permanently.

Output:

learnings

---

# Agent 17: Optimization Agent

Goal:
Improve future campaigns.

Uses:

* Analytics
* Learnings
* Historical Data

Creates:

* Better Hooks
* Better Thumbnails
* Better Scripts
* Better Videos

Output:

optimization

---

# Knowledge Base

Maintain permanent database of:

* Winning Hooks
* Winning CTAs
* Winning Video Lengths
* Winning Carousel Structures
* Winning Emotions
* Winning Platform Strategies

This database should continuously grow.

---

# Dashboard Requirements

Dashboard Pages:

1. Executive Overview
2. Campaign Management
3. Content Library
4. Agent Monitoring
5. Content Calendar
6. Platform Rules
7. Analytics
8. A/B Testing
9. Learnings
10. Brand Center
11. Approval Queue
12. Publishing Center

---

# Security Requirements

Implement:

* JWT Authentication
* RBAC
* Audit Logs
* Rate Limiting
* Secrets Management
* Secure API Storage
* Encryption at Rest
* Encryption in Transit

Roles:

* Admin
* Manager
* Content Reviewer
* Viewer

---

# Development Rules

1. Use modular architecture.
2. Every agent must be independently testable.
3. Every agent must have structured input/output.
4. Never hardcode platform rules.
5. Store all learnings.
6. Log all decisions.
7. Use async processing whenever possible.
8. Implement retry logic for external APIs.
9. Build for multi-client support.
10. Build for enterprise scale.

Success Metric:

The system should function as a self-improving AI Marketing Operating System that continuously researches, creates, publishes, analyzes, learns, and optimizes marketing campaigns for AI products and AI consultancy services.
