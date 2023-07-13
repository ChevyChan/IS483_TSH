import * as React from 'react';
import {
  ViewState,
  GroupingState,
  IntegratedGrouping,
} from '@devexpress/dx-react-scheduler';
import {
  Scheduler,
  WeekView,
  DayView,
  Appointments,
  Toolbar,
  DateNavigator,
  ViewSwitcher,
  AllDayPanel,
  AppointmentTooltip,
  AppointmentForm,
  GroupingPanel,
  Resources,
} from '@devexpress/dx-react-scheduler-material-ui';
import { connectProps } from '@devexpress/dx-react-core';
import { styled, alpha } from '@mui/material/styles';
import PriorityHigh from '@mui/icons-material/PriorityHigh';
import LowPriority from '@mui/icons-material/LowPriority';
import Lens from '@mui/icons-material/Lens';
import Event from '@mui/icons-material/Event';
import AccessTime from '@mui/icons-material/AccessTime';
import Paper from '@mui/material/Paper';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import Grid from '@mui/material/Grid';
import FormControl from '@mui/material/FormControl';
import classNames from 'clsx';

import { priorities } from './tasks';
import { event_info as tasks, getScheduleDetails, get_task_details} from './grouping';
import CustomStore from 'devextreme/data/custom_store';
import { HttpStatusCode } from 'axios';


const grouping = [{
  resourceName: 'priorityId',
}];

const filterTasks = (items, priorityId) => items.filter(task => (
  !priorityId || task.priorityId === priorityId
));

const getIconById = (id) => {
  if (id === 1) {
    return LowPriority;
  }
  if (id === 2) {
    return Event;
  }
  return PriorityHigh;
};

const PREFIX = 'Demo';
const classes = {
  flexibleSpace: `${PREFIX}-flexibleSpace`,
  prioritySelector: `${PREFIX}-prioritySelector`,
  content: `${PREFIX}-content`,
  contentContainer: `${PREFIX}-contentContainer`,
  text: `${PREFIX}-text`,
  title: `${PREFIX}-title`,
  icon: `${PREFIX}-icon`,
  contentItemIcon: `${PREFIX}-contentItemIcon`,
  grayIcon: `${PREFIX}-grayIcon`,
  colorfulContent: `${PREFIX}-colorfulContent`,
  lens: `${PREFIX}-lens`,
  textCenter: `${PREFIX}-textCenter`,
  dateAndTitle: `${PREFIX}-dateAndTitle`,
  titleContainer: `${PREFIX}-titleContainer`,
  container: `${PREFIX}-container`,
  bullet: `${PREFIX}-bullet`,
  prioritySelectorItem: `${PREFIX}-prioritySelectorItem`,
  priorityText: `${PREFIX}-priorityText`,
  priorityShortText: `${PREFIX}-priorityShortText`,
  cellLowPriority: `${PREFIX}-cellLowPriority`,
  cellMediumPriority: `${PREFIX}-cellMediumPriority`,
  cellHighPriority: `${PREFIX}-cellHighPriority`,
  headerCellLowPriority: `${PREFIX}-headerCellLowPriority`,
  headerCellMediumPriority: `${PREFIX}-headerCellMediumPriority`,
  headerCellHighPriority: `${PREFIX}-headerCellHighPriority`,
};
const stylesByPriority = priorities.reduce((acc, priority) => ({
  ...acc,
  [`cell${priority.text.replace(' ', '')}`]: {
    backgroundColor: alpha(priority.color[400], 0.1),
    '&:hover': {
      backgroundColor: alpha(priority.color[400], 0.15),
    },
    '&:focus': {
      backgroundColor: alpha(priority.color[400], 0.2),
    },
  },
  [`headerCell${priority.text.replace(' ', '')}`]: {
    backgroundColor: alpha(priority.color[400], 0.1),
    '&:hover': {
      backgroundColor: alpha(priority.color[400], 0.1),
    },
    '&:focus': {
      backgroundColor: alpha(priority.color[400], 0.1),
    },
  },
}), {});
const groupingStyles = ({ theme }) => ({
  [`&.${classes.cellLowPriority}`]: stylesByPriority.cellLowPriority,
  [`&.${classes.cellMediumPriority}`]: stylesByPriority.cellMediumPriority,
  [`&.${classes.cellHighPriority}`]: stylesByPriority.cellHighPriority,
  [`&.${classes.headerCellLowPriority}`]: stylesByPriority.headerCellLowPriority,
  [`&.${classes.headerCellMediumPriority}`]: stylesByPriority.headerCellMediumPriority,
  [`&.${classes.headerCellHighPriority}`]: stylesByPriority.headerCellHighPriority,
  [`& .${classes.icon}`]: {
    paddingLeft: theme.spacing(1),
    verticalAlign: 'middle',
  },
});

const StyledToolbarFlexibleSpace = styled(Toolbar.FlexibleSpace)(() => ({
  [`&.${classes.flexibleSpace}`]: {
    margin: '0 auto 0 0',
  },
}));

const StyledFormControl = styled(FormControl)(({ theme: { spacing } }) => ({
  [`&.${classes.prioritySelector}`]: {
    minWidth: 140,
    marginLeft: spacing(2),
    '@media (max-width: 500px)': {
      minWidth: 0,
      fontSize: '0.75rem',
      marginLeft: spacing(0.5),
    },
  },
}));

const StyledPrioritySelectorItem = styled('div')(({ theme: { palette, spacing }, color }) => ({
  [`& .${classes.bullet}`]: {
    backgroundColor: color ? color[400] : palette.divider,
    borderRadius: '50%',
    width: spacing(2),
    height: spacing(2),
    marginRight: spacing(2),
    display: 'inline-block',
  },
  [`&.${classes.prioritySelectorItem}`]: {
    display: 'flex',
    alignItems: 'center',
  },
  [`& .${classes.priorityText}`]: {
    '@media (max-width: 500px)': {
      display: 'none',
    },
  },
  [`& .${classes.priorityShortText}`]: {
    '@media (min-width: 500px)': {
      display: 'none',
    },
  },
}));
const StyledWeekViewTimeTableCell = styled(WeekView.TimeTableCell)(groupingStyles);
const StyledTooltipContent = styled('div')(({ theme: { spacing, typography, palette }, color }) => ({
  [`&.${classes.content}`]: {
    padding: spacing(3, 1),
    paddingTop: 0,
    backgroundColor: palette.background.paper,
    boxSizing: 'border-box',
    width: '400px',
  },
  [`& .${classes.contentContainer}`]: {
    paddingBottom: spacing(1.5),
  },
  [`& .${classes.text}`]: {
    ...typography.body2,
    display: 'inline-block',
  },
  [`& .${classes.title}`]: {
    ...typography.h6,
    color: palette.text.secondary,
    fontWeight: typography.fontWeightBold,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'normal',
  },
  [`& .${classes.icon}`]: {
    verticalAlign: 'middle',
  },
  [`& .${classes.contentItemIcon}`]: {
    textAlign: 'center',
  },
  [`& .${classes.grayIcon}`]: {
    color: palette.action.active,
  },
  [`& .${classes.colorfulContent}`]: {
    color: color[300],
  },
  [`& .${classes.lens}`]: {
    width: spacing(4.5),
    height: spacing(4.5),
    verticalAlign: 'super',
  },
  [`& .${classes.textCenter}`]: {
    textAlign: 'center',
  },
  [`& .${classes.dateAndTitle}`]: {
    lineHeight: 1.1,
  },
  [`& .${classes.titleContainer}`]: {
    paddingBottom: spacing(2),
  },
  [`& .${classes.container}`]: {
    paddingBottom: spacing(1.5),
  },
}));

const StyledDayViewDayScaleCell = styled(DayView.DayScaleCell)(groupingStyles);

const StyledWeekViewDayScaleCell = styled(WeekView.DayScaleCell)(groupingStyles);

const StyledAllDayPanelCell = styled(AllDayPanel.Cell)(groupingStyles);

const StyledGroupingPanelCell = styled(GroupingPanel.Cell)(groupingStyles);

const StyledDayViewTimeTableCell = styled(DayView.TimeTableCell)(groupingStyles);

const DayViewTimeTableCell = ({
  groupingInfo, ...restProps
}) => {
  const groupId = groupingInfo[0].id;
  return (
    <StyledDayViewTimeTableCell
      className={classNames({
        [classes.cellLowPriority]: groupId === 1,
        [classes.cellMediumPriority]: groupId === 2,
        [classes.cellHighPriority]: groupId === 3,
      })}
      groupingInfo={groupingInfo}
      {...restProps}
    />
  );
};
const DayViewDayScaleCell = ({
  groupingInfo, ...restProps
}) => {
  const groupId = groupingInfo[0].id;
  return (
    <StyledDayViewDayScaleCell
      className={classNames({
        [classes.headerCellLowPriority]: groupId === 1,
        [classes.headerCellMediumPriority]: groupId === 2,
        [classes.headerCellHighPriority]: groupId === 3,
      })}
      groupingInfo={groupingInfo}
      {...restProps}
    />
  );
};
const WeekViewTimeTableCell = ({
  groupingInfo, ...restProps
}) => {
  const groupId = groupingInfo[0].id;
  return (
    <StyledWeekViewTimeTableCell
      className={classNames({
        [classes.cellLowPriority]: groupId === 1,
        [classes.cellMediumPriority]: groupId === 2,
        [classes.cellHighPriority]: groupId === 3,
      })}
      groupingInfo={groupingInfo}
      {...restProps}
    />
  );
};
const WeekViewDayScaleCell = ({
  groupingInfo, ...restProps
}) => {
  const groupId = groupingInfo[0].id;
  return (
    <StyledWeekViewDayScaleCell
      className={classNames({
        [classes.headerCellLowPriority]: groupId === 1,
        [classes.headerCellMediumPriority]: groupId === 2,
        [classes.headerCellHighPriority]: groupId === 3,
      })}
      groupingInfo={groupingInfo}
      {...restProps}
    />
  );
};
const AllDayCell = ({
  groupingInfo, ...restProps
}) => {
  const groupId = groupingInfo[0].id;
  return (
    <StyledAllDayPanelCell
      className={classNames({
        [classes.cellLowPriority]: groupId === 1,
        [classes.cellMediumPriority]: groupId === 2,
        [classes.cellHighPriority]: groupId === 3,
      })}
      groupingInfo={groupingInfo}
      {...restProps}
    />
  );
};
const GroupingPanelCell = ({
  group, ...restProps
}) => {
  const groupId = group.id;
  const Icon = getIconById(groupId);
  return (
    <StyledGroupingPanelCell
      className={classNames({
        [classes.headerCellLowPriority]: groupId === 1,
        [classes.headerCellMediumPriority]: groupId === 2,
        [classes.headerCellHighPriority]: groupId === 3,
      })}
      group={group}
      {...restProps}
    >
      <Icon
        className={classes.icon}
      />
    </StyledGroupingPanelCell>
  );
};

const PrioritySelectorItem = ({
  color, text: resourceTitle,
}) => {
  const text = resourceTitle || 'All Tasks';
  const shortText = resourceTitle ? text.substring(0, 1) : 'All';

  return (
    <StyledPrioritySelectorItem className={classes.prioritySelectorItem} color={color}>
      <span className={classes.bullet} />
      <span className={classes.priorityText}>{text}</span>
      <span className={classes.priorityShortText}>{shortText}</span>
    </StyledPrioritySelectorItem>
  );
};

const PrioritySelector = ({
  priorityChange, priority,
}) => {
  const currentPriority = priority > 0 ? priorities[priority - 1] : {};
  return (
    <StyledFormControl className={classes.prioritySelector} variant="standard">
      <Select
        disableUnderline
        value={priority}
        onChange={(e) => {
          priorityChange(e.target.value);
        }}
        renderValue={() => (
          <PrioritySelectorItem text={currentPriority.text} color={currentPriority.color} />
        )}
      >
        <MenuItem value={0}>
          <PrioritySelectorItem />
        </MenuItem>
        {priorities.map(({ id, color, text }) => (
          <MenuItem value={id} key={id.toString()}>
            <PrioritySelectorItem color={color} text={text} />
          </MenuItem>
        ))}
      </Select>
    </StyledFormControl>
  );
};

const FlexibleSpace = (({
  priority, priorityChange, ...restProps
}) => (
  <StyledToolbarFlexibleSpace {...restProps} className={classes.flexibleSpace}>
    <PrioritySelector priority={priority} priorityChange={priorityChange} />
  </StyledToolbarFlexibleSpace>
));

// Modify this code by adding the function view data from Google Calendar only
const TooltipContent = ({
  appointmentData, formatDate, appointmentResources,
}) => {
  const resource = appointmentResources[0];
  let icon = <LowPriority className={classes.icon} />;
  if (appointmentData.priorityId === 2) {
    icon = <Event className={classes.icon} />;
  }
  if (appointmentData.priorityId === 3) {
    icon = <PriorityHigh className={classes.icon} />;
  }
  return (
    <StyledTooltipContent className={classes.content} color={resource.color}>
      <Grid container alignItems="flex-start" className={classes.titleContainer}>
        <Grid item xs={2} className={classNames(classes.textCenter)}>
          <Lens className={classNames(classes.lens, classes.colorfulContent)} />
        </Grid>
        <Grid item xs={10}>
          <div>
            <div className={classNames(classes.title, classes.dateAndTitle)}>
              {appointmentData.title}
            </div>
            <div className={classNames(classes.text, classes.dateAndTitle)}>
              {formatDate(appointmentData.startDate, { day: 'numeric', weekday: 'long' })}
            </div>
          </div>
        </Grid>
      </Grid>
      <Grid container alignItems="center" className={classes.contentContainer}>
        <Grid item xs={2} className={classes.textCenter}>
          <AccessTime className={classes.icon} />
        </Grid>
        <Grid item xs={10}>
          <div className={classes.text}>
            {`${formatDate(appointmentData.startDate, { hour: 'numeric', minute: 'numeric' })}
              - ${formatDate(appointmentData.endDate, { hour: 'numeric', minute: 'numeric' })}`}
          </div>
        </Grid>
      </Grid>
      <Grid container alignItems="center" key={`${resource.fieldName}_${resource.id}`}>
        <Grid
          className={classNames(classes.contentItemIcon, classes.icon, classes.colorfulContent)}
          item
          xs={2}
        >
          {icon}
        </Grid>
        <Grid item xs={10}>
          <span className={classNames(classes.text, classes.colorfulContent)}>
            {resource.text}
          </span>
        </Grid>
      </Grid>
    </StyledTooltipContent>
  );
};

export default class Demo extends React.PureComponent {
  constructor(props) {
    super(props);

    var date = new Date()
    var day = date.getDate()
    var month = date.getMonth() + 1
    var year = date.getFullYear()

    if (month.toString().length < 2) month = '0' + month;
    if (day.toString().length < 2) day = '0' + day;
    //console.log(`${year}-${month}-${day}`)

    // Get all the schedule from database
    getScheduleDetails()
    //get_task_details()

    this.state = {
      currentDate: `${year}-${month}-${day}`,
      currentViewName: 'Work Week',
      // Update 'tasks' attribute by linking with google events
      data: tasks,
      currentPriority: 0,
      resources: [{
        fieldName: 'priorityId',
        title: 'Priority',
        instances: priorities,
      }],
    };
    this.currentViewNameChange = (currentViewName) => {
      this.setState({ currentViewName });
    };
    this.currentDateChange = (currentDate) => {
      this.setState({ currentDate });
    };
    this.priorityChange = (value) => {
      const { resources } = this.state;
      const nextResources = [{
        ...resources[0],
        instances: value > 0 ? [priorities[value - 1]] : priorities,
      }];

      this.setState({ currentPriority: value, resources: nextResources });
    };
    this.flexibleSpace = connectProps(FlexibleSpace, () => {
      const { currentPriority } = this.state;
      return {
        priority: currentPriority,
        priorityChange: this.priorityChange,
      };
    });
  }

  componentDidUpdate() {
    this.flexibleSpace.update(); 
  }

  render() {
    const {
      data, currentDate, currentViewName, currentPriority, resources,
    } = this.state;

    return (
      <Paper>
        <Scheduler
          data={filterTasks(data, currentPriority)}
          height={860}
        >
          <ViewState
            currentDate={currentDate}
            currentViewName={currentViewName}
            onCurrentViewNameChange={this.currentViewNameChange}
            onCurrentDateChange={this.currentDateChange}
          />
          <GroupingState
            grouping={grouping}
          />

          <DayView
            startDayHour={9}
            endDayHour={19}
            timeTableCellComponent={DayViewTimeTableCell}
            dayScaleCellComponent={DayViewDayScaleCell}
            intervalCount={2}
          />
          <WeekView
            startDayHour={9}
            endDayHour={17}
            excludedDays={[0, 6]}
            name="Work Week"
            timeTableCellComponent={WeekViewTimeTableCell}
            dayScaleCellComponent={WeekViewDayScaleCell}
          />
          <AllDayPanel
            cellComponent={AllDayCell}
          />

          <Appointments />
          <Resources
            data={resources}
          />
          <IntegratedGrouping />

          <GroupingPanel
            cellComponent={GroupingPanelCell}
          />
          <Toolbar flexibleSpaceComponent={this.flexibleSpace} />
          <DateNavigator />
          <ViewSwitcher />
          <AppointmentTooltip
            contentComponent={TooltipContent}
            showOpenButton
            showCloseButton
          />
          <AppointmentForm />
        </Scheduler>
      </Paper>
    );
  }
}


// import 'whatwg-fetch';
// import React from 'react';
// import * as cred_details from './is483-tsh-387702-e204a8a0451f.json';

// import Scheduler from 'devextreme-react/scheduler';

// import CustomStore from 'devextreme/data/custom_store';

// function getData(_, requestOptions) {
//   const PUBLIC_KEY = 'AIzaSyBnNAISIUKe6xdhq1_rjor2rxoI3UlMY7k'; // To be replaced with own Public Key
//   const CALENDAR_ID = 'f7jnetm22dsjc3npc2lu3buvu4@group.calendar.google.com'; // To be replaced with own Calendar ID
//   const dataUrl = ['https://www.googleapis.com/calendar/v3/calendars/',
//     CALENDAR_ID, '/events?key=', PUBLIC_KEY].join('');

//   return fetch(dataUrl, requestOptions).then(
//     (response) => response.json(),
//   ).then((data) => data.items);
// }

// const dataSource = new CustomStore({
//   load: (options) => getData(options, { showDeleted: false }),
// });

// const currentDate = new Date(2017, 4, 25);
// const views = ['day', 'workWeek', 'month'];

// class MyCalendar extends React.Component {
//   render() {
//     return (
//       <React.Fragment>
//         <div className="long-title">
//           <h3>Delivery Scheduler - TSH Pte Ltd</h3>
//         </div>
//         <Scheduler
//           dataSource={dataSource}
//           views={views}
//           defaultCurrentView="workWeek"
//           defaultCurrentDate={currentDate}
//           height={500}
//           startDayHour={7}
//           editing={false}
//           showAllDayPanel={false}
//           startDateExpr="start.dateTime"
//           endDateExpr="end.dateTime"
//           textExpr="summary"
//           timeZone="America/Los_Angeles" />
//       </React.Fragment>

//     );
//   }
// }

// export default MyCalendar;

