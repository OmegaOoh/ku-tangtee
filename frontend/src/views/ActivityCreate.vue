<template>
<div class="flex items-center justify-center min-h-screen">
    <div class="card bg-neutral card-primary w-96 shadow-xl items-center">
        <div class="card-body">
            <h2 class="class-title">Create Activity</h2>
            <label>Activity Name
            <input 
                v-model="activityName"
                type="text" 
                placeholder="Activity Name" 
                class="input input-bordered input-primary w-full max-w-xs mb-4" 
            />
            </label>
            <label>Activity Detail
            <textarea 
                v-model="activityDetail"
                class="textarea textarea-primary w-full max-w-xs mb-4" 
                placeholder="Activity Detail">
            </textarea>
            </label>
            <label>Date and Time
            <VueDatePicker 
                v-model="date"
                type="text"
                placeholder="Select Date" 
                :min-date="new Date()"
            />
            </label>
            <label>Max People
            <input 
                v-model.number="maxPeople"
                type="number" 
                placeholder="Enter Max People (Optional)" 
                class="input input-bordered input-primary w-full max-w-xs mb-4"
                :min="0"
            />
            </label>
            <button class="btn btn-primary" @click="logData">Create Activity</button>
            <button class="btn btn-secondary" @click="goBack">Back to List</button>
        </div>
    </div>
</div>
</template>


<script>
export default {
    data() {
        return {
            activityName: '',
            activityDetail: '',
            date: '',
            maxPeople: 0,
        };
    },
    methods: {
        goBack() {
            /*
             * Navigate back to Activity Index page.
             * This function does not return anything.
             */
            this.$router.push("/");
        },
        logData() {
            if (this.max_people < 0) {
                this.max_people = 0;
            }
                console.log('Activity Name:', this.activityName);
                console.log('Activity Detail:', this.activityDetail);
                console.log('Selected Date:', this.date);
                console.log('Max People:', this.maxPeople);
        },
    }
}
</script>