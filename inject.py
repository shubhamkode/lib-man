# database Service
from src.shared.database_service import DatabaseService

from src.features.book.data.sources.local.local_book_source import LocalBookSource
from src.features.student.data.sources.local.local_student_source import (
    LocalStudentDataSource,
)


# repositories
from src.features.book.data.repository.book_repository_impl import BookRepositoryImpl
from src.features.student.data.repositories.student_repo_impl import (
    StudentRepositoryImpl,
)


# usecases
from src.features.book.domain.usecases import (
    CreateNewBookUseCase,
    GetAllBooksUseCase,
    DeleteBookByIdUseCase,
    GetBookByIdUseCase,
    UpdateBookByIdUseCase,
    UpdateBookRecordUseCase,
)

from src.features.student.domain.usecases import (
    CreateNewStudentUseCase,
    GetAllStudentsUseCase,
    DeleteStudentByIdUseCase,
    UpdateStudentByIdUseCase,
    GetStudentByIdUseCase,
    UpdateStudentRecordUseCase,
)


# views
from src.features.book.presentation.book_view import BookView
from src.features.student.presentation.student_view import StudentView
from src.features.record.presentation.record_view import RecordView


def inject(dbClient: DatabaseService):
    ## datasources
    book_source = LocalBookSource(dbClient)
    student_source = LocalStudentDataSource(dbClient)

    ## repositories
    book_repository = BookRepositoryImpl(book_source)
    student_repo = StudentRepositoryImpl(student_source)

    ## usecases
    get_all_books_usecase = GetAllBooksUseCase(book_repository)
    get_book_by_id_usecase = GetBookByIdUseCase(book_repository)
    delete_book_by_id_usecase = DeleteBookByIdUseCase(book_repository)
    create_new_book_usecase = CreateNewBookUseCase(book_repository)
    update_book_by_id_usecase = UpdateBookByIdUseCase(book_repository)
    update_book_record_usecase = UpdateBookRecordUseCase(book_repository)

    create_new_student_usecase = CreateNewStudentUseCase(student_repo)
    get_all_students_usecase = GetAllStudentsUseCase(student_repo)
    get_student_by_id_usecase = GetStudentByIdUseCase(student_repo)
    update_student_by_id_usecase = UpdateStudentByIdUseCase(student_repo)
    delete_student_by_id_usecase = DeleteStudentByIdUseCase(student_repo)
    update_student_record_usecase = UpdateStudentRecordUseCase(student_repo)

    book_view = BookView(
        create_new_book_usecase=create_new_book_usecase,
        get_all_books_usecase=get_all_books_usecase,
        get_book_by_id_usecase=get_book_by_id_usecase,
        update_book_by_id_usecase=update_book_by_id_usecase,
        delete_book_by_id_usecase=delete_book_by_id_usecase,
        get_student_by_id_usecase=get_student_by_id_usecase,
    )

    student_view = StudentView(
        create_new_student_usecase=create_new_student_usecase,
        get_all_students_usecase=get_all_students_usecase,
        get_student_by_id_usecase=get_student_by_id_usecase,
        update_student_by_id_usecase=update_student_by_id_usecase,
        delete_student_by_id_usecase=delete_student_by_id_usecase,
        get_book_by_id_usecase=get_book_by_id_usecase,
    )

    record_view = RecordView(
        update_student_record_usecase=update_student_record_usecase,
        update_book_by_id_usecase=update_book_by_id_usecase,
        get_book_by_id_usecase=get_book_by_id_usecase,
        get_student_by_id_usecase=get_student_by_id_usecase,
        update_book_record_usecase = update_book_record_usecase
    )

    return [book_view, student_view, record_view]
