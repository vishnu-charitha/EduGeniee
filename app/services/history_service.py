from app.database import crud


def save_ai_history(
    db,
    user_id,
    task,
    prompt,
    response
):

    try:

        crud.save_history(

            db=db,
            user_id=user_id,
            task=task,
            prompt=prompt,
            response=response

        )

    except Exception as e:

        print("History Save Error:", e)