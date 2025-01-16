./
├── frontend/
│   ├── node_modules/
│   │   └── vuetify/
│   │       ├── lib/
│   │       │   ├── components/
│   │       │   └── composables/
│   │       │       └── date/
│   │       └── styles/
│   ├── public/
│   └── src/
│       ├── api/
│       ├── assets/
│       ├── components/
│       │   └── __tests__/
│       ├── mocks/
│       ├── router/
│       ├── stores/
│       └── views/
├── infrastructure/
│   ├── terraform/
│   │   ├── .terraform/
│   │   │   └── providers/
│   │   ├── bootstrap/
│   │   ├── dev/
│   │   ├── environments/
│   │   │   ├── dev/
│   │   │   └── prod/
│   │   ├── github-oidc/
│   │   └── modules/
│   │       ├── agile_stories/
│   │       ├── api_gateway/
│   │       ├── dynamodb/
│   │       ├── lambda/
│   │       ├── sqs/
│   │       ├── step_functions/
│   │       └── vpc/
├── scripts/
│   └── generate_docs.py



All files:


./
├── frontend/
│   ├── node_modules/
│   │   └── vuetify/
│   │       ├── lib/
│   │       │   ├── components/
│   │       │   │   └── VNoSsr/
│   │       │   │       ├── VNoSsr.mjs
│   │       │   │       └── VNoSsr.mjs.map
│   │       │   ├── composables/
│   │       │   │   └── date/
│   │       │   │       ├── DateAdapter.mjs
│   │       │   │       └── DateAdapter.mjs.map
│   │       │   └── styles/
│   │       │       ├── elements/
│   │       │       │   └── _blockquote.sass
│   │       │       ├── generic/
│   │       │       │   └── _animations.scss
│   │       │       └── utilities/
│   │       │           └── _elevation.scss
│   │       └── styles/
│   │           └── settings/
│   │               └── _elevations.scss
│   ├── public/
│   │   ├── favicon.ico
│   │   └── sticky_note_2_24dp_FFFF55_FILL0_wght400_GRAD0_opsz24.svg
│   └── src/
│       ├── api/
│       │   ├── api.ts
│       │   ├── storyApi.js
│       │   └── storyApi.ts
│       ├── assets/
│       │   └── base.css
│       ├── components/
│       │   ├── DevNav.vue
│       │   ├── HelloWorld.vue
│       │   ├── RouterDebug.vue
│       │   ├── TheWelcome.vue
│       │   ├── WelcomeItem.vue
│       │   ├── __tests__/
│       │   │   └── HelloWorld.spec.ts
│       │   └── icons/
│       │       ├── IconCommunity.vue
│       │       ├── IconDocumentation.vue
│       │       ├── IconEcosystem.vue
│       │       ├── IconSupport.vue
│       │       └── IconTooling.vue
│       ├── mocks/
│       │   ├── mockAnalysisData.ts
│       │   ├── mockFormatData.ts
│       │   └── mockTechReviewData.ts
│       ├── router/
│       ├── stores/
│       │   ├── counter.js
│       │   ├── counter.ts
│       │   ├── story.ts
│       │   ├── storyStore.js
│       │   └── storyStore.ts
│       └── views/
│           ├── AboutView.vue
│           ├── AgileReview.vue
│           ├── Backup polling
│           ├── Estimates.vue
│           ├── HomeView.vue
│           ├── StoryInput copy.vue
│           ├── StoryTestView.vue
│           ├── TechReview.vue
│           ├── TestAgileResults.vue
│           ├── TestEstimateView.vue
│           ├── TestFormatView.vue
│           ├── TestTechReview.vue
│           ├── TestTechReviewView.vue
│           └── TestView.vue
├── infrastructure/
│   ├── terraform/
│   │   ├── .terraform/
│   │   │   └── providers/
│   │   │       └── registry.terraform.io/
│   │   │           └── hashicorp/
│   │   │               └── aws/
│   │   │                   └── 5.83.1/
│   │   │                       └── darwin_arm64/
│   │   │                           └── terraform-provider-aws_v5.83.1_x5
│   │   ├── bootstrap/
│   │   │   ├── bootstrap.sh
│   │   │   └── terraform.tfstate
│   │   ├── dev/
│   │   │   ├── api_gateway.tf
│   │   │   └── frontend.tf
│   │   ├── environments/
│   │   │   ├── dev/
│   │   │   │   ├── backend.tf
│   │   │   │   ├── plan.txt
│   │   │   │   ├── remove_vpc_config.sh
│   │   │   │   ├── ssm-policy.json
│   │   │   │   ├── stepfunctions-policy.json
│   │   │   │   ├── terraform-user-policies.json
│   │   │   │   ├── variables.tf.backup
│   │   │   │   └── workflow.json
│   │   │   └── prod/
│   │   ├── github-oidc/
│   │   │   ├── terraform.tfstate.backup
│   │   │   └── tfplan
│   │   └── modules/
│   │       ├── agile_stories/
│   │       ├── api_gateway/
│   │       │   └── integrations.tf
│   │       ├── dynamodb/
│   │       ├── lambda/
│   │       │   └── main.tf.bak2
│   │       ├── sqs/
│   │       │   ├── alarms.tf
│   │       │   └── dashboard.tf
│   │       ├── step_functions/
│   │       │   ├── story_analysis copy.json
│   │       │   ├── story_analysis.json
│   │       │   └── variable.tf
│   │       └── vpc/
├── scripts/
│   └── generate_docs.py
