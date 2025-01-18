cd /Users/dhogan/Development\ Projects/agile-stories-v2/frontend/
npm run build
aws s3 sync dist/ s3://dev-agile-stories-frontend
aws cloudfront create-invalidation \
    --distribution-id E2BP3G13C91WFS \
    --paths "/*"
    