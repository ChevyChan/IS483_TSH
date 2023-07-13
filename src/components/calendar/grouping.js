import { HttpStatusCode } from "axios"

export var event_info = [
  // {
  //   title: 'Website Re-Design Plan',
  //   priorityId: 2,
  //   startDate: new Date(2023, 7, 10, 9, 30),
  //   endDate: new Date(2023, 7, 10, 11, 30),
  //   id: 0,
  // }
]

export async function get_calendar_details() {
  try{
    const response = await fetch('http://localhost:5002/v1/google_calendar/retrieve_default_calendar', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Error! status: ${response.status}`);
    }

    // 2) await the .json() call to get the data
    const result = await response.json();
    console.log(result)
    return result;

  } catch (err) {
    console.log(err);
  }
}

// retrieve all the task details from database
export async function get_task_details(){
  try{  
    const response = await fetch('http://localhost:5001/v1/calendar_tasks/get_all_calendar_tasks', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Error! status: ${response.status}`);
    }

    // 2) await the .json() call to get the data
    const result = await response.json();
    console.log(result)
    return result;

  } catch (err) {
    console.log(err);
  }
}

export function create_task(task_uuid, task_name, task_date, task_time, task_description, priority_level, user_uid, calendar_uid) {
  try{
    fetch('http://localhost:5001/v1/calendar_tasks/create_calendar_task', {
      method: 'POST',
      mode: "no-cors",
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        "task_uuid": task_uuid, 
        "task_name": task_name, 
        "task_date": task_date, 
        "task_time": task_time, 
        "task_description": task_description,
        "priority_level": priority_level, 
        "task_completed": 'needsAction', 
        "user_uid": user_uid, 
        "calendar_uid": calendar_uid
      }
    })
    .then(response => {
      if(!HttpStatusCode.Ok) {
        throw new Error("Bad Request. Please try again!")
      }
    })
    .then(result => {
      console.log(result)
      return result
    })
  } catch(err) {
    console.log(err)
  }
}

// Retrieve all scheduling details for delivery from database
export async function getScheduleDetails(){
  try{  
    const response = await fetch('http://localhost:5003/v1/schedule/get_all_schedule', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Error! status: ${response.status}`);
    }

    // 2) await the .json() call to get the data
    const result = await response.json();
    console.log(result)
    return result;

  } catch (err) {
    console.log(err);
  }
}

// Retrieve all event details from google calendar
export async function getEventDetailsFromGoogleCalendar(calendarId){
  try{  
    const response = await fetch('http://localhost:5002/v1/google_calendar/retrieve_calendar_events/' + calendarId, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Error! status: ${response.status}`);
    }

    // 2) await the .json() call to get the data
    const result = await response.json();
    console.log(result)
    return result;

  } catch (err) {
    console.log(err);
  }
}

// Retrieve all existing tasks from google calendar
export async function getTaskDetailsFromGoogleCalendar(taskLists){
  try{
    const response = await fetch('http://localhost:5004/v1/google_tasks/retrieve_tasks/' + taskLists)

    if (!response.ok) {
      throw new Error(`Error! status: ${response.status}`);
    }

    const result = await response.json();
    //console.log(result)
    return result

  } catch (err) {
    console.log(err)
  }
}

// Sync tasks with google tasks / google calendar
export function sync_tasks_with_google(taskListId, title, dueDate) {
  try {
    fetch('http://localhost:5004/v1/google_tasks/create_tasks/' + taskListId + "/" + title + "/" + dueDate, {
      method: 'POST',
      mode: "no-cors",
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        "status": "needsAction", 
        "title": title,
        "due": dueDate
      }
    })
    .then(response => {
      if(!HttpStatusCode.Ok) {
        throw new Error("Bad Request. Please try again!")
      }
    })
    .then(result => {
      console.log(result)
      return result
    })
  } catch(err) {
    console.log(err)
  } 
}

// Sync events from database to google calendar
export function sync_with_google_calendar(calendarId, summary, location, description, startTime, endTime){
  try{
    fetch('http://localhost:5002/v1/google_calendar/create_calendar_events/' + calendarId + "/" + summary + "/" + location + "/" + description + "/" + startTime + "/" + endTime, {
      method: 'POST',
      mode: "no-cors",
      headers: {
        'Content-Type': 'application/json'
      },
      body: {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
          'dateTime': startTime,
          'timeZone': 'Singapore',
        },
        'end': {
          'dateTime': endTime,
          'timeZone': 'Singapore',
        }
      }
    })
    .then(response => {
      if(!HttpStatusCode.Ok){
        throw new Error("Bad Request.")
      }
    }).then(data => {
      console.log(data)
      return data
    })
    .catch(error => {
      console.log(error)
    })
  } catch (err) {
    console.log(err);
  }
}

// This function to be added to frontend of creating tasks. ** Test this function first ** 
function create_new_task(user_uid, task_name, task_period_date, task_period_time, task_description, priority_level){
  const result = sync_tasks_with_google("MDU2NTM3NTk5NTIwNDUzODE5OTM6MDow", task_name, 
  task_period_date + "T" + task_period_time + "Z")

  var task_id = result['id']
  var task_title = result['title']
  var task_date = result['due'].slice(0,9)
  var task_time = result['due'].slice(11,18)
  var calendar_uid = ""

  get_calendar_details().then(response => {
    // Get google calendar id from Google API function
    calendar_uid = response['id']
  })
  
  // After the tasks is added, disable the "Add to Task" button at frontend
  create_task(task_id, task_title, task_date, task_time, task_description, priority_level, user_uid, calendar_uid)
}

// // Get all the task details from database and store in a dictionary to reflect on the calendar
// get_task_details().then(data => {
//   for (let task_details in data['data']["Calendar_Tasks_Details"]){
//     var startDate = data['data']['Calendar_Tasks_Details'][parseInt(task_details)]['task_date']
//     var startTime = data['data']['Calendar_Tasks_Details'][parseInt(task_details)]['task_time']
//     var endDate = data['data']['Calendar_Tasks_Details'][parseInt(task_details)]['task_date']
//     var endTime = data['data']['Calendar_Tasks_Details'][parseInt(task_details)]['task_time']

//     event_info.push({
//       title: data['data']['Calendar_Tasks_Details'][parseInt(task_details)]['task_name'],
//       priorityId: parseInt(data['data']['Calendar_Tasks_Details'][parseInt(task_details)]['priority_level']),
//       startDate: new Date(startDate.slice(0,4), startDate.slice(5,7) - 1, startDate.slice(8,10), startTime.slice(0,2), startTime.slice(3,5)),
//       endDate: new Date(endDate.slice(0,4), endDate.slice(5,7) - 1, endDate.slice(8,10), endTime.slice(0,2), endTime.slice(3,5)),
//       id: data['data']['Calendar_Tasks_Details'][parseInt(task_details)]['task_uuid']
//     })
//   }
// })

// Retrieve all the scheduling details from database and store it in a dictionary to display at the frontend calendar
getScheduleDetails().then(data => {

  for (let event_details in data['data']['Scheduling_List']) {

    var startDate = data['data']['Scheduling_List'][parseInt(event_details)]['schedule_start_date']
    var startTime = data['data']['Scheduling_List'][parseInt(event_details)]['schedule_start_time']
    var endDate = data['data']['Scheduling_List'][parseInt(event_details)]['schedule_end_date']
    var endTime = data['data']['Scheduling_List'][parseInt(event_details)]['schedule_end_time']

    // var adj_start_date = new Date(startDate.slice(0,4), startDate.slice(5,7) - 1, startDate.slice(8,10) - 1)
    // var adj_start_time = data['data']['Scheduling_List'][parseInt(event_details)]['schedule_start_time'].slice(0,8)
    // var adj_end_date = new Date(endDate.slice(0,4), endDate.slice(5,7) - 1 , endDate.slice(8,10) - 1)
    // var adj_end_time =  data['data']['Scheduling_List'][parseInt(event_details)]['schedule_end_time'].slice(0,5)

    // console.log(adj_start_date + " | " + adj_start_time + ", " + adj_end_date + " | " + adj_end_time)

    console.log(data['data']['Scheduling_List'][parseInt(event_details)]['schedule_summary'] + " | " + startDate)
  
    event_info.push({
      title: data['data']['Scheduling_List'][parseInt(event_details)]['schedule_summary'],
      priorityId: parseInt(data['data']['Scheduling_List'][parseInt(event_details)]['priority_level']),
      startDate: new Date(startDate.slice(0,4), startDate.slice(5,7) - 1, startDate.slice(8,10), startTime.slice(0,2), startTime.slice(3,5)),
      endDate: new Date(endDate.slice(0,4), endDate.slice(5,7) - 1 , endDate.slice(8,10), endTime.slice(0,2), endTime.slice(3,5)),
      id: data['data']['Scheduling_List'][parseInt(event_details)]['delivery_uid']
    })
    // Note: When the scheduling algorithm is executed, only run the job once. For subsequent jobs, it will be for other deliveries that have not been executed.
    // Check back on this again. There's still a bug (e.g., Bad Request) in the algorithm.
    sync_with_google_calendar("chevychan1@gmail.com", 
    data['data']['Scheduling_List'][parseInt(event_details)]['schedule_summary'], 
    data['data']['Scheduling_List'][parseInt(event_details)]['schedule_to_location'], 
    data['data']['Scheduling_List'][parseInt(event_details)]['schedule_description'], 
    startDate + 'T' + startTime.slice(0,12), 
    endDate + 'T' + endTime.slice(0,12))
  }

  // Re-check the date and timing. Does not tally with database data
  // getEventDetailsFromGoogleCalendar("chevychan1@gmail.com").then(response =>{
  //   console.log(response)
    // if(response.length == 0){
    //   for(let event_details in data['data']['Scheduling_List']){
    //     sync_with_google_calendar("chevychan1@gmail.com", 
    //     data['data']['Scheduling_List'][parseInt(event_details)]['schedule_summary'], 
    //     data['data']['Scheduling_List'][parseInt(event_details)]['schedule_to_location'], 
    //     data['data']['Scheduling_List'][parseInt(event_details)]['schedule_description'], 
    //     startDate + 'T' + startTime.slice(0,12), 
    //     endDate + 'T' + endTime.slice(0,12))
        // console.log(data['data']['Scheduling_List'][parseInt(event_details)]['schedule_summary'], 
        // data['data']['Scheduling_List'][parseInt(event_details)]['schedule_to_location'], 
        // data['data']['Scheduling_List'][parseInt(event_details)]['schedule_description'], 
        // startDate + 'T' + startTime.slice(0,5), 
        // endDate + 'T' + endTime.slice(0,5))
      // }
    // }
    // for(let event_details in data['data']['Scheduling_List']){
    //   // for(let event in response){
    //   //   //console.log(response[event])
    //   //   // Checking error. Need to debug
    //   //   if(response[event] == data['data']['Scheduling_List'][parseInt(event_details)]['schedule_summary'] + " | " + startDate){
    //   //     console.log("Schedule exist. Please verify.")
    //   //     return
    //   //   }else{
    //   //     console.log("Oh no!")
    //       // console.log(data['data']['Scheduling_List'][parseInt(event_details)]['schedule_summary'], 
    //       // data['data']['Scheduling_List'][parseInt(event_details)]['schedule_to_location'], 
    //       // data['data']['Scheduling_List'][parseInt(event_details)]['schedule_description'], 
    //       // startDate + 'T' + startTime.slice(0,5), 
    //       // endDate + 'T' + endTime.slice(0,5))
    //       sync_with_google_calendar("chevychan1@gmail.com", 
    //       data['data']['Scheduling_List'][parseInt(event_details)]['schedule_summary'], 
    //       data['data']['Scheduling_List'][parseInt(event_details)]['schedule_to_location'], 
    //       data['data']['Scheduling_List'][parseInt(event_details)]['schedule_description'], 
    //       startDate + 'T' + startTime.slice(0,12), 
    //       endDate + 'T' + endTime.slice(0,12))
    //     }
      // }
  //   }
  // })
  console.log(event_info)
})