import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import IconPrev from '@material-ui/icons/NavigateBefore';
import IconNext from '@material-ui/icons/NavigateNext';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { connect } from 'react-redux';
import { withLayout } from '../../components/Layout';
import { OverlayCircularProgress } from '../../components/OverlayCircularProgress';
import { caseList } from '../../lib/redux/actions/';
import { deepGet } from '../../lib/utils';
import CaseListTable from './CaseListTable';
import FilterBox from './FilterBox';
import { useStyles } from './styles';

const CaseListPage = ({ loadCaseList, list, loading }) => {
  const classes = useStyles();
  const [ filter, setFilter ] = useState({});
  const [ page, setPage ] = useState(1);

  const { hasNext, hasPrevious, cases } = useMemo(() => ({
    hasNext: deepGet(list, 'next') !== undefined,
    hasPrevious: deepGet(list, 'previous') !== undefined,
    cases: deepGet(list, 'results', []),
  }), [ list ]);

  useEffect(() => {
    loadCaseList({ ...filter, page });
  }, [ loadCaseList, filter, page ]);


  const handleChangeFilter = useCallback((filter) => {
    setPage(1);
    setFilter(filter);
  }, []);

  return <>
    <Paper className={ classes.titlePaper }>
      <Typography variant='h4' component={ 'span' } className={ classes.whiteText }>
        Lista cazurilor&nbsp;
      </Typography>
    </Paper>
    <Paper className={ classes.filterPaper }>
      <FilterBox onChange={ handleChangeFilter }/>
    </Paper>
    <Paper className={ classes.contentPaper }>
      <Box className={ classes.tableBox }>
        <CaseListTable data={ cases }/>
      </Box>
      <Box className={ classes.buttonBox }>
        <Button disabled={ !hasPrevious } onClick={ () => setPage(page - 1) }>
          <IconPrev/> Prec.
        </Button>
        <Button disabled={ !hasNext } onClick={ () => setPage(page + 1) }>
          <IconNext/> Urm.
        </Button>
      </Box>
      <OverlayCircularProgress show={ loading } circularSize={ 100 }/>
    </Paper>
  </>;
};

const mapStateToProps = state => {
  return {
    list: state.caseList.caseList,
    loading: state.caseList.caseListLoading,
    errors: state.caseList.caseListErrors,
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadCaseList: (filters) => {
      dispatch(caseList.loadCaseList(filters));
    },
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(withLayout(CaseListPage));

