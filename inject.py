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
    BookCreateUseCase,
    BookGetAllUseCase,
    BookGetUseCase,
    BookUpdateUseCase,
    BookDeleteUseCase,
    BookUpdateRecordUseCase
)


from src.features.student.domain.usecases import (
    StudentCreateUseCase,
    StudentGetAllUseCase,
    StudentGetUseCase,
    StudentUpdateUseCase,
    StudentDeleteUseCase,
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
    book_repo = BookRepositoryImpl(book_source)
    student_repo = StudentRepositoryImpl(student_source)

    ## usecases
    book_create_usecase = BookCreateUseCase(book_repo)
    book_get_all_usecase = BookGetAllUseCase(book_repo)
    book_get_usecase = BookGetUseCase(book_repo)
    book_update_usecase = BookUpdateUseCase(book_repo)
    book_delete_usecase = BookDeleteUseCase(book_repo)

    student_create_usecase = StudentCreateUseCase(student_repo)
    student_get_all_usecase = StudentGetAllUseCase(student_repo)
    student_get_usecase = StudentGetUseCase(student_repo)
    student_update_usecase = StudentUpdateUseCase(student_repo)
    student_delete_usecase = StudentDeleteUseCase(student_repo)

    update_student_record_usecase = UpdateStudentRecordUseCase(student_repo)
    book_update_record_usecase = BookUpdateRecordUseCase(book_repo)

    book_view = BookView(
        book_create_usecase=book_create_usecase,
        book_get_all_usecase=book_get_all_usecase,
        book_get_usecase=book_get_usecase,
        book_update_usecase=book_update_usecase,
        book_delete_usecase=book_delete_usecase,
        student_get_usecase=student_get_usecase,
    )

    student_view = StudentView(
        student_create_usecase=student_create_usecase,
        student_get_all_usecase=student_get_all_usecase,
        student_get_usecase=student_get_usecase,
        student_update_usecase=student_update_usecase,
        student_delete_usecase=student_delete_usecase,
        book_get_usecase=book_get_usecase,
    )

    record_view = RecordView(
        book_get_usecase=book_get_usecase,
        book_update_usecase=book_update_usecase,
        student_get_usecase=student_get_usecase,

        book_update_record_usecase = book_update_record_usecase,
        update_student_record_usecase=update_student_record_usecase,
    )

    return (book_view, student_view, record_view)
