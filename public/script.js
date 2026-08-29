async function predictValue() {

    const predictionElement =
        document.getElementById("prediction");

    predictionElement.innerText = "Predicting...";


    const data = {

        overall:
            Number(
                document.getElementById("overall").value
            ),

        potential:
            Number(
                document.getElementById("potential").value
            ),

        age:
            Number(
                document.getElementById("age").value
            ),

        international_reputation:
            Number(
                document.getElementById(
                    "international_reputation"
                ).value
            ),

        pace:
            Number(
                document.getElementById("pace").value
            ),

        shooting:
            Number(
                document.getElementById("shooting").value
            ),

        passing:
            Number(
                document.getElementById("passing").value
            ),

        dribbling:
            Number(
                document.getElementById("dribbling").value
            ),

        physic:
            Number(
                document.getElementById("physic").value
            ),

        skill_moves:
            Number(
                document.getElementById("skill_moves").value
            )
    };


    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        if (!response.ok) {

            const errorText =
                await response.text();

            console.error(
                "API Error:",
                errorText
            );

            throw new Error(
                "Prediction API failed: " +
                response.status
            );
        }


        const result =
            await response.json();


        predictionElement.innerText =
            "€" +
            Number(
                result.predicted_value_million
            ).toFixed(2) +
            " Million";


    }

    catch (error) {

        console.error(
            "Prediction error:",
            error
        );

        predictionElement.innerText =
            "Prediction failed";
    }

}