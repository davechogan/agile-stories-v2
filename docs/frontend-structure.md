# Frontend Directory Structure

## Overview

### frontend/
Active development directory for v2. This is our primary frontend codebase.

```
frontend/
├── src/
│   ├── api/
│   │   └── storyApi.ts           # Story API methods
│   │
│   ├── components/
│   │   └── [core components]     # Shared components
│   │
│   ├── router/
│   │   └── index.ts              # Vue Router configuration
│   │
│   ├── stores/
│   │   └── story.ts              # Story state management
│   │
│   └── views/
│       ├── StoryInput.vue        # Story submission
│       ├── AgileReview.vue       # INVEST analysis
│       └── TechReview.vue        # Technical review
```

### frontend-src/
Reference code from v1 project. Kept for:
- Code reference
- Component reuse
- Pattern examples

**Note:** This directory is not actively used in development. It serves as a reference only and could be archived once v2 is complete.

## Next Steps
1. Complete v2 frontend implementation
2. Archive frontend-src/ directory
3. Update documentation to focus on active frontend/ structure
4. Clean up any unused components copied from v1 