// Types matching our Lambda response
interface EstimateValue {
  value: number;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
}

interface RoleEstimate {
  role: string;
  name: string;
  title: string;
  estimates: {
    story_points: EstimateValue;
    person_days: EstimateValue;
  };
  justification: Array<{
    title: string;
    content: string;
  }>;
  avatarUrl: string;
}

interface EstimateResponse {
  story_id: string;
  average: number;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  individual_estimates: RoleEstimate[];
}

// Fun name components
const adjectives = [
  'Quantum', 'Binary', 'Cosmic', 'Digital', 'Cyber', 'Neural', 'Vector', 
  'Pixel', 'Circuit', 'Matrix', 'Data', 'Cloud', 'Static', 'Dynamic',
  'Crypto', 'Sonic', 'Hyper', 'Mega', 'Ultra', 'Techno'
];

const nouns = [
  'Bot', 'Byte', 'Core', 'Node', 'Chip', 'Grid', 'Link', 'Net', 'Port',
  'Pulse', 'Wave', 'Spark', 'Beam', 'Unit', 'Loop', 'Stack', 'Cache',
  'Flux', 'Gear', 'Prism'
];

const generateName = (): string => {
  const adj = adjectives[Math.floor(Math.random() * adjectives.length)];
  const noun = nouns[Math.floor(Math.random() * nouns.length)];
  return `${adj} ${noun}`;
};

const avatarStyles = [
  'bottts',        // Robots
  'bottts-neutral', // More robots
  'shapes',        // Abstract shapes
  'identicon',     // GitHub-style identicons
  'icons',         // Abstract icons
  'pixel-art',     // Pixel art creatures (non-human)
  'thumbs',        // Abstract thumbprint patterns
];

// First, let's get roles from settings (we'll mock it for now)
const getSelectedRoles = () => [
  { role: 'backend_dev', title: 'Backend Developer' },
  { role: 'frontend_dev', title: 'Frontend Developer' },
  { role: 'devops_engineer', title: 'DevOps Engineer' },
  { role: 'qa_engineer', title: 'QA Engineer' },
  { role: 'security_expert', title: 'Security Expert' },
  { role: 'database_admin', title: 'Database Administrator' }
  // We'll get this from settings later
];

// Mock data generator
export const getMockEstimates = (storyId: string): EstimateResponse => {
  const selectedRoles = getSelectedRoles();
  const mockTeam: RoleEstimate[] = selectedRoles.map(roleInfo => ({
    role: roleInfo.role,
    name: generateName(),
    title: roleInfo.title,
    estimates: {
      story_points: { 
        value: Math.floor(Math.random() * 13) + 3, // Random estimate between 3-15
        confidence: ['HIGH', 'MEDIUM', 'LOW'][Math.floor(Math.random() * 3)] as 'HIGH' | 'MEDIUM' | 'LOW'
      },
      person_days: {
        value: Math.floor(Math.random() * 14) + 2, // Random estimate between 2-15 days
        confidence: ['HIGH', 'MEDIUM', 'LOW'][Math.floor(Math.random() * 3)] as 'HIGH' | 'MEDIUM' | 'LOW'
      }
    },
    justification: getRoleJustification(roleInfo.role),
    avatarUrl: `https://api.dicebear.com/7.x/${avatarStyles[Math.floor(Math.random() * avatarStyles.length)]}/svg?seed=${roleInfo.role}`
  }));

  // Calculate mock average
  const useStoryPoints = Math.random() > 0.5; // randomly choose for testing
  const estimateType = useStoryPoints ? 'story_points' : 'person_days';
  const values = mockTeam.map(member => member.estimates[estimateType].value);
  const average = values.reduce((a, b) => a + b, 0) / values.length;

  return {
    story_id: storyId,
    average,
    confidence: 'HIGH',
    individual_estimates: mockTeam
  };
};

// Role-specific justifications
const getRoleJustification = (role: string) => {
  const justifications: Record<string, Array<{title: string, content: string}>> = {
    'backend_dev': [
      {
        title: 'API Changes',
        content: 'Need to implement new endpoints and modify existing ones for the new functionality.'
      },
      {
        title: 'Database Impact',
        content: 'Schema modifications required with careful migration planning.'
      }
    ],
    'frontend_dev': [
      {
        title: 'UI Components',
        content: 'New reusable components needed with responsive design considerations.'
      },
      {
        title: 'State Management',
        content: 'Updates to global state and data flow patterns required.'
      }
    ],
    'devops_engineer': [
      {
        title: 'Infrastructure Changes',
        content: 'Need to update deployment pipelines and monitoring systems.'
      },
      {
        title: 'Performance Monitoring',
        content: 'Additional metrics and alerts need to be configured.'
      }
    ],
    // ... add more role-specific justifications
  };

  return justifications[role] || [
    {
      title: 'General Considerations',
      content: 'Standard implementation and testing time allocated.'
    }
  ];
}; 