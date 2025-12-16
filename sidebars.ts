import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'modules/module-1-ros2/chapter-1',
        'modules/module-1-ros2/chapter-2',
        'modules/module-1-ros2/chapter-3',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin & Simulation',
      items: [
        'modules/module-2-simulation/chapter-1',
        'modules/module-2-simulation/chapter-2',
        'modules/module-2-simulation/chapter-3',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: AI Robot Brain (NVIDIA Isaac)',
      items: [
        'modules/module-3-isaac/chapter-1',
        'modules/module-3-isaac/chapter-2',
        'modules/module-3-isaac/chapter-3',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action Systems',
      items: [
        'modules/module-4-vla/chapter-1',
        'modules/module-4-vla/chapter-2',
        'modules/module-4-vla/chapter-3',
      ],
    },
  ],
};

export default sidebars;
