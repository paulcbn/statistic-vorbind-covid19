import ColorlessDeleteIcon from '@material-ui/icons/Clear';
import React from 'react';
import { useDeleteIconStyle } from './styles';

const DeleteIcon = () => {
  const classes = useDeleteIconStyle();
  return <ColorlessDeleteIcon className={ classes.icon }/>;
};
export default DeleteIcon;

