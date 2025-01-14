1. Component-Level Styles (Highest Priority)
   └─ <style scoped> in .vue files
   └─ Inline styles
   └─ Component-specific classes

2. Router-Level Settings
   └─ router/index.js
      └─ Route meta fields
      └─ Layout configurations
      └─ Transition settings

3. Vuetify Configuration (main.js)
   └─ Theme settings
   └─ Default component settings
   └─ Breakpoints
   └─ Display settings
   └─ Global Vuetify classes (.v-application, .v-main, etc.)

4. Global App Styles (App.vue)
   └─ Application-wide layouts
   └─ Common component styles
   └─ Layout structure (.v-app, .v-main)

5. Global CSS Files (Lowest Priority)
   └─ main.css (imported in main.js)
   └─ base.css (imported in main.css)
   └─ Vuetify styles (imported in main.js)

Override Order:
- More specific selectors override less specific ones
- Later imports override earlier ones
- !important declarations override normal declarations

Load Order:
1. base.css (fundamental styles)
   ↓
2. main.css (imports base.css, adds global styles)
   ↓
3. Vuetify default styles (from node_modules)
   ↓
4. App.vue styles (application structure)
   ↓
5. Router configurations (layout structure)
   ↓
6. Component styles (most specific)

Key Points:
- Scoped styles only affect their component
- Global styles affect everything
- Vuetify classes can be overridden but require proper specificity
- Router settings affect how components are mounted and transitioned
- main.js configuration affects how Vuetify behaves globally

## Common Layout Patterns

### Two-Column Layout
Used in: AgileReview.vue, TechReview.vue, TestAgileResults.vue

Template Structure:
    <template>
      <div class="two-column-layout">
        <!-- Left Column -->
        <div class="primary-content-wrapper">
          <div class="primary-content">
            <!-- Content here -->
          </div>
        </div>

        <!-- Right Column -->
        <div class="analysis-panel">
          <!-- Analysis content here -->
        </div>
      </div>
    </template>

Critical CSS Properties:
    .two-column-layout {
      display: grid;
      grid-template-columns: 1fr 1fr;  /* Flexible columns */
      gap: 2rem;
      padding: 2rem;
      max-width: 1800px;
      margin: 0 auto;
      min-height: 100vh;
    }

    .primary-content-wrapper, .analysis-panel {
      width: 100%;
      min-width: 0;  /* Critical: Prevents overflow issues */
    }

    .primary-content {
      background: rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      padding: 2rem;
      overflow-y: auto;
    }

### Common Issues & Solutions

1. Layout Breaking at Small Screens
   Problem: Content overflows or columns don't resize properly
   Solution: 
    @media (max-width: 1024px) {
      .two-column-layout {
        grid-template-columns: 1fr;  /* Stack columns */
      }
    }

2. Content Overflow
   Problem: Content breaks out of containers
   Solution:
   - Add min-width: 0 to column wrappers
   - Use overflow-y: auto for scrollable content

3. Responsive Design
   Problem: Fixed widths causing layout issues
   Solution:
   - Use 1fr instead of fixed pixel widths
   - Implement proper media queries
   - Avoid minmax() with fixed minimums

### Best Practices

1. Grid Layout
   - Use 1fr 1fr for flexible columns
   - Avoid fixed minimum widths
   - Include proper gap spacing

2. Wrapper Elements
   - Always include min-width: 0
   - Set width: 100%
   - Use consistent padding

3. Content Containers
   - Consistent border-radius (12px)
   - Consistent background opacity
   - Proper padding (2rem)

4. Loading States
    <template>
      <v-fade-transition>
        <div v-if="!analysis" class="loading">
          <v-progress-circular/>
        </div>
        <div v-else class="two-column-layout">
          <!-- Content -->
        </div>
      </v-fade-transition>
    </template>

### Development Tips

1. Mock Data Usage
   - Use mockAnalysisData.ts for development
   - Comment out polling logic during frontend work
   - Document backend dependencies

2. Component Testing
   - Test layouts at various screen sizes
   - Verify overflow handling
   - Check transition states