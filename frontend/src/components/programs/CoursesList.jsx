import './styles/CoursesList.css'
import CourseCard from "./CourseCard";
import LoadingSpinner from "../common/LoadingSpinner";
import Error from "../common/Error";
import EmptyResult from "../common/EmptyResult";

const CoursesList = ({courses, loading, error}) => {

    if (loading) {
        return (
            <LoadingSpinner
                input="курсов">
            </LoadingSpinner>
        );
    }

    if (error) {
        return (
            <Error
            message="Не удалось загрузить дисциплины">
            </Error>
        );
    }

    return (
        <div className="courses-list-container">
            {courses.length === 0 ? (
                <EmptyResult
                    header="Дисциплины не найдены">
                </EmptyResult>
            ) : (
                <>
                    <div className="cl-grid">
                        {courses.map((course) => (
                            <CourseCard key={course.id} course={course} />
                        ))}
                    </div>

                </>
                )}
        </div>
    );

}
export default CoursesList;
