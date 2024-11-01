<template>
    <div class="breadcrumbs text-lm size-fit my-6 mx-10 w-full h-fit overflow-visible">
        <ul>
            <li><a @click="$router.push('/');">Home</a></li>
            <li>Profile</li>
        </ul>
    </div>
    <div
        class="card p-2 bg-base-300 border-2 border-primary shadow-md rounded-lg m-6"
    >
        <div class="card-body">
            <div class="card p-4 bg-base-100 shadow-md rounded-lg w-full">
                <div class='card-body flex flex-row justify-start w-full'>
                    <div>
                        <div class="avatar indicator">
                            <p class="indicator-item indicator-bottom indicator-center badge badge-accent font-semibold">
                                KU 83
                            </p>
                        
                            <div class="w-24 rounded-md">
                                <img v-lazy="'https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp'" />
                            </div>
                        </div>
                    </div>
                    <div class='flex-row ml-3 w-full'>
                        <span class="text-2xl font-semibold text-wrap break-words"> FirstName LastName </span>
                        <span class="text-xs font-light"> user616621263186424 </span>
                        <div>
                            <p class=" text-primary break-words text-wrap"> Engineering </p>
                            <p class="text-sm font-light text-accent break-words text-wrap"> Software and Knowledge Engineering</p>
                        </div>
                        <div>
                            <p class="pt-2 text-sm font-semibold">Bio</p>
                            <textarea class="text-xs w-full resize-none bg-inherit overflow-hidden break-normal" disabled rows="2">
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis,.
                            </textarea>
                        </div>
                    </div>
                </div>
            </div>
            <div class="divider">
                Joined Activity
            </div>
            <div class="flex flex-col">
                <div class="card bg-base-200 w-full border-2 border-base-200 hover:border-primary transition-all ease-in-out duration-200">
                    <div class="card-body">
                        <h2 class="card-title line-clamp-1">
                            Activity Name
                        </h2>
                        <p class="line-clamp-2">The description of activity I don't want to write.</p>
                        <p>
                            <strong>Date and Time: </strong>
                            Sunday, Nov 3, 2024, 09:00 am
                        </p>
                    </div>


                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}

.line-clamp-1 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    line-clamp: 1;
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
