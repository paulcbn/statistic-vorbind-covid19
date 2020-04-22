import AccountIcon from '@material-ui/icons/AccountCircle';
import SettingsIcon from '@material-ui/icons/Settings';
import { userTypes } from '../../lib/constants';

export const getProfileRoute = userType => {
  if (userType === userTypes.DOCTOR)
    return '/doctor/profile';

  if (userType === userTypes.PATIENT)
    return '/patient/profile';

  return '/';
};
export const getDashboardRoute = userType => {
  if (userType === userTypes.DOCTOR)
    return '/doctor';

  if (userType === userTypes.PATIENT)
    return '/patient';

  return '/';
};

const doctorMenuSections = [
  {
    title: 'General', entries: [
      { name: 'Dashboard', route: '/doctor' },
      { name: 'Engaged patients', route: '/doctor/engaged-patients' },
    ],
  },
  {
    title: 'Configuration', entries: [
      { name: 'Profile', route: '/doctor/profile', Icon: AccountIcon },
      { name: 'Settings', route: '/doctor/settings', Icon: SettingsIcon },
    ],
  },
];

const patientMenuSections = [
  {
    title: 'Configuration', entries: [
      { name: 'Profile', route: '/doctor/profile', Icon: AccountIcon },
      { name: 'Settings', route: '/doctor/settings', Icon: SettingsIcon },
    ],
  },
];

export const getMenuSections = userType => {
  if (userType === userTypes.DOCTOR)
    return doctorMenuSections;

  if (userType === userTypes.PATIENT)
    return patientMenuSections;

  return [];
};
