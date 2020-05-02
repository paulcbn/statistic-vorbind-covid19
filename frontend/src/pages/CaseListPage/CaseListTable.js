import { TableContainer } from '@material-ui/core';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import React, { useCallback } from 'react';
import { COUNTIES } from '../../config/countyInfo';
import { deepGet } from '../../lib/utils';
import { useStyles } from './styles';

const GENDERS = {
  'M': 'Bărbat',
  'F': 'Femeie',
};

const columns = [
  {
    key: 'caseNumber',
    label: 'Nr. caz',
    formatter: entry => deepGet(entry, 'caseNumber', '-'),
  },
  {
    key: 'age',
    label: 'Vârsta',
    formatter: entry => deepGet(entry, 'age', '-'),
  },
  {
    key: 'gender',
    label: 'Sex',
    formatter: entry => {
      const genderCode = deepGet(entry, 'gender');
      return genderCode !== undefined ? GENDERS[genderCode] : '-';
    },
  },
  {
    key: 'county',
    label: 'Județ',
    formatter: entry => {
      const countyCode = deepGet(entry, 'county');
      return countyCode !== undefined ? COUNTIES[countyCode] : '-';
    },
  },
  {
    key: 'hospitalAdmissionDate',
    label: 'Data internării',
    formatter: entry => deepGet(entry, 'hospitalAdmissionDate', '-'),
  },
  {
    key: 'testDate',
    label: 'Data testării',
    formatter: entry => deepGet(entry, 'testDate', '-'),
  },
  {
    key: 'positiveResultDate',
    label: 'Data confirmării',
    formatter: entry => deepGet(entry, 'positiveResultDate', '-'),
  },
  {
    key: 'deathDate',
    label: 'Data decesului',
    formatter: entry => deepGet(entry, 'deathDate', '-'),
  },
  {
    key: 'source',
    label: 'Sursa',
    formatter: entry => <a href={deepGet(entry, 'source.url')} target='_blank' rel="noopener noreferrer">Link</a>,
  },
];


const CaseListTable = ({ data }) => {

  const classes = useStyles();

  const renderRows = useCallback(() => {
    return (data || []).map(value => {
      return <TableRow hover>
        { columns.map(c => <TableCell key={ c.key }>{ c.formatter(value) }</TableCell>) }
      </TableRow>;
    });
  }, [ data ]);

  return <TableContainer>
    <Table className={ classes.table } size="small">
      <TableHead>
        <TableRow>
          { columns.map(c => <TableCell className={ classes.tableHeaderCell } key={ c.key }>{ c.label }</TableCell>) }
        </TableRow>
      </TableHead>
      <TableBody>
        { renderRows() }
      </TableBody>
    </Table>
  </TableContainer>;
};

export default CaseListTable;
