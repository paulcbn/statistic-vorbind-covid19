import { FormGroup, Input } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import Divider from '@material-ui/core/Divider';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormLabel from '@material-ui/core/FormLabel';
import Grid from '@material-ui/core/Grid';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import Select from '@material-ui/core/Select';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from '@material-ui/core/Typography';
import React, { useMemo, useState } from 'react';
import { COUNTIES } from '../../config/countyInfo';
import { useStyles } from './styles';

const FILTER_ALL = '*';

const GenderInput = ({ value, setValue }) => {
  return <FormControl component="fieldset">
    <FormLabel component="legend">Gen</FormLabel>
    <RadioGroup value={ value } onChange={ (event) => setValue(event.target.value) }>
      <FormControlLabel value="F" control={ <Radio/> } label="Femei"/>
      <FormControlLabel value="M" control={ <Radio/> } label="Bărbați"/>
      <FormControlLabel value={ FILTER_ALL } control={ <Radio/> } label="Ambele"/>
    </RadioGroup>
  </FormControl>;
};

const CountyInput = ({ value, setValue }) => {
  const classes = useStyles();

  return <FormControl className={ classes.selectControl }>
    <InputLabel>Județ</InputLabel>
    <Select
      value={ value }
      onChange={ (event) => setValue(event.target.value) }
    >
      <MenuItem value={ FILTER_ALL } key={ FILTER_ALL }>Toate</MenuItem>
      { Object.entries(COUNTIES)
        .map(([ code, name ]) => <MenuItem value={ code } key={ code }>{ name }</MenuItem>,
        ) }
    </Select>
    <FormHelperText>Alege județul</FormHelperText>
  </FormControl>;
};

const ValidatedInput = ({ value, setValue }) => {

  return <FormControl>
    <FormControlLabel
      control={
        <Checkbox
          checked={ value }
          onChange={ (event) => setValue(event.target.checked) }
          name="Cazuri validate manual"
          color="primary"
        />
      }
      label="Cazuri validate manual"/>
  </FormControl>;
};

const AgeBetweenInput = ({ value1, setValue1, value2, setValue2 }) => {

  return <FormGroup>
    <FormControl>
      Vârsta minimă:
      <Input type={ 'number' } value={ value1 } onChange={ (event => setValue1(event.target.value)) }/>
    </FormControl>
    <FormControl>
      Vârsta maximă:
      <Input type={ 'number' } value={ value2 } onChange={ (event => setValue2(event.target.value)) }/>
    </FormControl>
  </FormGroup>;
};


const FilterBox = ({ onChange }) => {
  const classes = useStyles();
  const [ gender, setGender ] = useState(FILTER_ALL);
  const [ county, setCounty ] = useState(FILTER_ALL);
  const [ validated, setValidated ] = useState(false);
  const [ ageLowBound, setAgeLowBound ] = useState(0);
  const [ ageHighBound, setAgeHighBound ] = useState(100);

  const filters = useMemo(() => {
    let result = {
      gender: gender,
      county__icontains: county,
      validated: validated ? 'True' : FILTER_ALL,
      age__gte: ageLowBound,
      age__lte: ageHighBound,
    };

    Object.keys(result).forEach(key => {
      if (result[key] === FILTER_ALL)
        delete result[key];
    });
    return result;
  }, [ gender, county, validated, ageLowBound, ageHighBound ]);

  return <ExpansionPanel className={classes.expansionPanel}>
    <ExpansionPanelSummary
      expandIcon={ <ExpandMoreIcon/> }
    >
      <Typography color='primary' variant={'h5'}>Filtre</Typography>
    </ExpansionPanelSummary>
    <ExpansionPanelDetails>
      <Grid container>
        <Grid item xs={ 12 } className={ classes.dividerBox }>
          <Divider/>
        </Grid>
        <Grid item xs={ 12 } sm={ 6 } md={ 3 } className={ classes.gridItems }>
          <CountyInput value={ county } setValue={ setCounty }/>
        </Grid>
        <Grid item xs={ 12 } sm={ 6 } md={ 3 } className={ classes.gridItems }>
          <GenderInput setValue={ setGender } value={ gender }/>
        </Grid>
        <Grid item xs={ 12 } sm={ 6 } md={ 3 } className={ classes.gridItems }>
          <ValidatedInput setValue={ setValidated } value={ validated }/>
        </Grid>
        <Grid item xs={ 12 } sm={ 6 } md={ 3 } className={ classes.gridItems }>
          <AgeBetweenInput setValue1={ setAgeLowBound } value1={ ageLowBound }
                           setValue2={ setAgeHighBound } value2={ ageHighBound }/>
        </Grid>
        <Grid item xs={ 12 } className={ classes.gridItems }>
          <Button variant='contained' color='secondary' size='large' onClick={ () => onChange(filters) }>
            Aplică
          </Button>
        </Grid>
      </Grid>
    </ExpansionPanelDetails>
  </ExpansionPanel>;
};

export default FilterBox;
