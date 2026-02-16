import './styles/CoursesList.css'
import CourseCard from "./CourseCard";

const CoursesList = ({courses, loading, error}) => {

    if (loading) {
        return (
            <div className="loading-container">
                    <div className="loading-spinner"></div>
                <p>Загрузка курсов...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="error-container">
                    <div className="error-icon">❌</div>
                    <h3>Ошибка загрузки курсов</h3>
                </div>
        );
    }

    return (
        <div className="courses-list-container">
            {courses.length === 0 ? (
                <div className="no-results">
                    <div className="no-results-icon">📭</div>
                    <h3>Дисциплины не найдены</h3>
                </div>
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
