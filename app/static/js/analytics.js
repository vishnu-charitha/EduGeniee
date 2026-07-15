async function loadAnalytics(){

    const token = localStorage.getItem("token");

    const response = await fetch("/analytics/",{

        headers:{

            Authorization:`Bearer ${token}`

        }

    });

    const data = await response.json();

    new Chart(

        document.getElementById("analyticsChart"),

        {

            type:"bar",

            data:{

                labels:[

                    "Questions",

                    "Quiz",

                    "Summary",

                    "Learning"

                ],

                datasets:[{

                    label:"Usage",

                    data:[

                        data.questions,

                        data.quizzes,

                        data.summaries,

                        data.learning_paths

                    ]

                }]

            }

        }

    );

}