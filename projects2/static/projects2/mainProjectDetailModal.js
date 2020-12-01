Vue.component("modal", {
  template: "#modal-template",
  delimiters: ["${", "}"],
  props: {
    mtype: {
      type: String,
      required: true,
    },
    year: {
      type: Object,
      required: true,
    },
    my_staff: {
      type: Object,
      required: false,
    },
    my_om_cost: {
      type: Object,
      required: false,
    },
    my_capital_cost: {
      type: Object,
      required: false,
    },
    my_gc_cost: {
      type: Object,
      required: false,
    },
    my_activity: {
      type: Object,
      required: false,
    },
    my_collaborator: {
      type: Object,
      required: false,
    },
    my_agreement: {
      type: Object,
      required: false,
    },
    my_status_report: {
      type: Object,
      required: false,
    },
    my_file: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      currentUser: null,
      isACRDP: false,
      staff: {
        name: null,
        user: null,
        funding_source: this.year.default_funding_source_id,
        is_lead: false,
        employee_type: null,
        level: null,
        duration_weeks: null,
        overtime_hours: null,
        overtime_description: null,
        student_program: null,
        amount: 0,
      },
      errors: null,
      disableNameField: false,
      disableStudentProgramField: false,
      disableAmountField: false,
      disableLevelField: false,
      projectLeadWarningIssued: false,
      showOTCalc: false,
      dates: [],
      dates_loading: false,
      new_ot_desc: null,

      //cal field but for some reason cannot use computed fields
      totalOTHours: 0,
      totalOTCalcHours: 0,
      totalOTDescription: "",

      // om costs
      om_cost: {
        funding_source: this.year.default_funding_source_id,
        om_category: "",
        description: "",
        amount: 0,
      },

      // capital costs
      capital_cost: {
        funding_source: this.year.default_funding_source_id,
        category: "",
        description: "",
        amount: 0,
      },

      // gc costs
      gc_cost: {
        recipient_org: null,
        project_lead: null,
        proposed_title: null,
        gc_program: null,
        amount: 0,
      },

      // activities
      activity: {
        name: "",
        description: "",
        target_date: null,
      },

      // collaborators
      collaborator: {
        name: "",
        critical: false,
        notes: null,
      },

      // agreements
      agreement: {
        partner_organization: null,
        project_lead: null,
        agreement_title: null,
        new_or_existing: null,
        notes: null,
      },

      // status reports
      status_report: {
        status: null,
        major_accomplishments: null,
        major_issues: null,
        target_completion_date: null,
        rationale_for_modified_completion_date: null,
        general_comment: null,
        section_head_comment: null,
        section_head_reviewed: null,
      },

      // files
      fileToUpload: null,
      file: {
        name: null,
        external_url: null,
      },
    }
  },
  methods: {
    onFileChange() {
      this.fileToUpload = this.$refs.file.files[0];
    },

    onSubmit() {
      this.errors = null
      if (this.mtype === "staff") {
        if (this.my_staff) {
          let endpoint = `/api/project-planning/staff/${this.my_staff.id}/`;
          apiService(endpoint, "PATCH", this.staff).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/staff/`;
          apiService(endpoint, "POST", this.staff).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }
      // om cost
      else if (this.mtype === "om_cost") {
        if (this.my_om_cost) {
          let endpoint = `/api/project-planning/om-costs/${this.my_om_cost.id}/`;
          apiService(endpoint, "PATCH", this.om_cost).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/om-costs/`;
          apiService(endpoint, "POST", this.om_cost).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }
      // capital cost
      else if (this.mtype === "capital_cost") {
        if (this.my_capital_cost) {
          let endpoint = `/api/project-planning/capital-costs/${this.my_capital_cost.id}/`;
          apiService(endpoint, "PATCH", this.capital_cost).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/capital-costs/`;
          apiService(endpoint, "POST", this.capital_cost).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }

      // gc cost
      else if (this.mtype === "gc_cost") {
        if (this.my_gc_cost) {
          let endpoint = `/api/project-planning/gc-costs/${this.my_gc_cost.id}/`;
          apiService(endpoint, "PATCH", this.gc_cost).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/gc-costs/`;
          apiService(endpoint, "POST", this.gc_cost).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }

      // activity
      else if (this.mtype === "activity") {
        if (this.activity.target_date === "") this.activity.target_date = null
        if (this.my_activity) {
          let endpoint = `/api/project-planning/activities/${this.my_activity.id}/`;
          apiService(endpoint, "PATCH", this.activity).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/activities/`;
          apiService(endpoint, "POST", this.activity).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }

      // collaborator
      else if (this.mtype === "collaborator") {
        if (this.my_collaborator) {
          let endpoint = `/api/project-planning/collaborators/${this.my_collaborator.id}/`;
          apiService(endpoint, "PATCH", this.collaborator).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/collaborators/`;
          apiService(endpoint, "POST", this.collaborator).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }

      // agreement
      else if (this.mtype === "agreement") {
        if (this.my_agreement) {
          let endpoint = `/api/project-planning/agreements/${this.my_agreement.id}/`;
          apiService(endpoint, "PATCH", this.agreement).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/agreements/`;
          apiService(endpoint, "POST", this.agreement).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }

      // status report
      else if (this.mtype === "status_report") {
        if (this.status_report.target_completion_date === "") this.status_report.target_completion_date = null
        if (this.status_report.section_head_reviewed == null) this.status_report.section_head_reviewed = "False"
        console.log(this.status_report.target_completion_date)

        if (this.my_status_report) {
          let endpoint = `/api/project-planning/status-reports/${this.my_status_report.id}/`;
          apiService(endpoint, "PATCH", this.status_report).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/status-reports/`;
          apiService(endpoint, "POST", this.status_report).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }


      // file
      else if (this.mtype === "file") {
        if (this.my_file) {
          // if there is a file attribute, delete it since we send back the file through a separate request
          if (this.file.file) delete this.file.file

          let endpoint = `/api/project-planning/files/${this.my_file.id}/`;
          apiService(endpoint, "PATCH", this.file).then(response => {
            if (response.id) {
              if (this.fileToUpload) {
                fileApiService(endpoint, "PATCH", "file", this.fileToUpload)
                this.fileToUpload = null
              }
              this.$emit('close')
            } else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/files/`;
          apiService(endpoint, "POST", this.file).then(response => {
            if (response.id) {
              // now we have to upload the file
              if (this.fileToUpload) {
                let endpoint = `/api/project-planning/files/${response.id}/`;
                fileApiService(endpoint, "PATCH", "file", this.fileToUpload)
                this.fileToUpload = null
              }
              this.$emit('close')
            } else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }


      }
    },
    adjustStaffFields() {

      // if not a student, disable the student program field
      if (this.staff.employee_type !== "4") {
        this.staff.student_program = null;
        this.disableStudentProgramField = true;
      } else {
        this.disableStudentProgramField = false;
      }

      // if employee type is fte, disable "cost" field and the "level" field.
      // do the same If they are a seasonal indeterminate  paid from a-base
      if (this.staff.employee_type == 1 || (this.staff.employee_type == 6 && this.staff.funding_source == 1)) {
        this.staff.amount = null;
        this.disableAmountField = true;
        this.staff.level = null;
        this.disableLevelField = true;
      } else {
        this.disableAmountField = false;
        this.disableLevelField = false;
      }


      // if there is a DFO user, disable the text name field
      if (this.staff.user) {
        this.staff.name = null;
        this.disableNameField = true;
      } else {
        this.disableNameField = false;
      }

      // if the current user is changing themselves away from project lead, give them a warning
      // only do this if we are editing an existing user
      if (this.my_staff) {
        if (this.currentUser && this.currentUser.id == this.my_staff.user && !this.projectLeadWarningIssued && this.staff.is_lead === "False") {
          alert(warningMsg);
          this.projectLeadWarningIssued = true
        }
      }

    },
    toggleOTCalc() {
      this.showOTCalc = !this.showOTCalc;
      // if the modal is open, let's fetch the dates
      if (this.showOTCalc) this.getDates(this.year.fiscal_year);
    },
    getDates(fiscalYearId) {
      this.dates_loading = true;
      let endpoint = `/api/project-planning/get-dates/?year=${fiscalYearId}`;
      apiService(endpoint)
          .then(response => {
            this.dates_loading = false;
            this.dates = response;
          })
    },
    processOT() {
      userInput = confirm(processOTMsg)
      if (userInput) {
        this.staff.overtime_hours = this.totalOTCalcHours;
        this.staff.overtime_description = this.totalOTDescription.replaceAll("<br>", "\n");
        this.toggleOTCalc()
      }
    },
    updateDate(date) {
      // we need 2 things: calculated OT and description of OT
      if (date.is_stat || date.int_weekdy === "0") {
        date.calc_ot = date.ot_hours * 2
        date.ot_description = `${date.short_weekday} ${date.formatted_short_date}: ${date.ot_hours}h x 2 = ${date.calc_ot}h`
        if (date.is_stat) date.ot_description += " (stat.)<br>"
        else date.ot_description += "<br>"
      } else {
        // a little more complicated
        if (date.int_weekday === "6" && Number(date.ot_hours) > 7.5) {
          diff = date.ot_hours - 7.5
          date.calc_ot = (7.5 * 1.5) + diff * 2
          date.ot_description = `${date.short_weekday} ${date.formatted_short_date}: 7.5h x 1.5 = 11.25h<br>`
          date.ot_description += `${date.short_weekday} ${date.formatted_short_date}: ${diff}h x 2 = ${Number(diff) * 2}h<br>`
        } else {
          date.calc_ot = date.ot_hours * 1.5
          date.ot_description = `${date.short_weekday} ${date.formatted_short_date}: ${date.ot_hours}h x 1.5 = ${date.calc_ot}h<br>`
        }
      }

      // total OT hours
      this.totalOTHours = 0;
      this.totalOTCalcHours = 0;
      this.totalOTDescription = "";
      for (var i = 0; i < this.dates.length; i++) {
        var d = this.dates[i];
        if (d.ot_hours) this.totalOTHours += Number(d.ot_hours)
        if (d.calc_ot) this.totalOTCalcHours += Number(d.calc_ot)
        if (d.ot_description) this.totalOTDescription += d.ot_description
      }
    },
    getCurrentUser() {
      let endpoint = `/api/project-planning/user/`;
      apiService(endpoint)
          .then(response => {
            this.currentUser = response;
          })
    },
    populateTargetDate(quarter){
      sap_year = this.year.fiscal_year
      if(quarter === "q1") {
        this.activity.target_date = `${sap_year-1}-06-30`
      } else if(quarter === "q2") {
        this.activity.target_date = `${sap_year-1}-09-30`
      } else if(quarter === "q3") {
        this.activity.target_date = `${sap_year-1}-12-31`
      } else if(quarter === "q4") {
        this.activity.target_date = `${sap_year}-03-31`
      }

    },
  },
  computed: {},
  created() {

    this.getCurrentUser();

    if (this.year.project.default_funding_source.toLowerCase().search("acrdp") > -1) {
      this.isACRDP = true;
    }

    this.$nextTick(() => {
      if (this.mtype === "staff") {
        if (this.my_staff && this.my_staff.id) {
          this.staff = this.my_staff
          // there is an annoying thing that has to happen to convert the html to js to pytonese...
          if (this.staff.is_lead) this.staff.is_lead = "True"
          else this.staff.is_lead = "False"
        }
        this.adjustStaffFields()
      }
      // om costs
      else if (this.mtype === "om_cost") {
        if (this.my_om_cost && this.my_om_cost.id) {
          this.om_cost = this.my_om_cost
        }
      }
      // capital costs
      else if (this.mtype === "capital_cost") {
        if (this.my_capital_cost && this.my_capital_cost.id) {
          this.capital_cost = this.my_capital_cost
        }
      }
      // gc costs
      else if (this.mtype === "gc_cost") {
        if (this.my_gc_cost && this.my_gc_cost.id) {
          this.gc_cost = this.my_gc_cost
        }
      }

      // activities
      else if (this.mtype === "activity") {
        if (this.my_activity && this.my_activity.id) {
          this.activity = this.my_activity
          // there is an annoying thing that has to happen to convert the html to js to pytonese...
          if (this.activity.target_date) this.activity.target_date = this.activity.target_date.slice(0, 10)
          else this.activity.target_date = null
        }
      }
      // collaborators
      else if (this.mtype === "collaborator") {
        if (this.my_collaborator && this.my_collaborator.id) {
          this.collaborator = this.my_collaborator
          // there is an annoying thing that has to happen to convert the html to js to pytonese...
          if (this.collaborator.critical) this.collaborator.critical = "True"
          else this.collaborator.critical = "False"
        }
      }
      // agreements
      else if (this.mtype === "agreement") {
        if (this.my_agreement && this.my_agreement.id) {
          this.agreement = this.my_agreement
          // there is an annoying thing that has to happen to convert the html to js to pytonese...
          if (this.agreement.critical) this.agreement.critical = "True"
          else this.agreement.critical = "False"
        }
      }

      // status reports
      else if (this.mtype === "status_report") {
        if (this.my_status_report && this.my_status_report.id) {
          this.status_report = this.my_status_report
          // there is an annoying thing that has to happen to convert the html to js to pytonese...
          if (this.status_report.section_head_reviewed) this.status_report.section_head_reviewed = "True"
          else this.status_report.section_head_reviewed = "False"
          // there is an annoying thing that has to happen to convert the html to js to pytonese...
          if (this.status_report.target_completion_date) this.status_report.target_completion_date = this.status_report.target_completion_date.slice(0, 10)
          else this.status_report.target_completion_date = null
        }
      }

      // files
      else if (this.mtype === "file") {
        if (this.my_file && this.my_file.id) {
          this.file = this.my_file
        }
      }

    })


  },

});