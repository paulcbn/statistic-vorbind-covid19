import { makeStyles } from '@material-ui/core';

export const useDeleteIconStyle = makeStyles((theme) => ({
  icon: {
    color: theme.palette.error.main,
  },
}));