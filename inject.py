# database Service
from src.shared.database_service import DatabaseService


# repositories
from src.features.book.controller import BookRepoImpl

from src.features.student.controller import StudentRepoImpl


from src.core.main_app import MainAppWrapper
from src.features.auth import AuthScreenWrapper
from src.shared.screens.home.home_screen import HomeScreenWrapper
from src.features.book.view import BookWrapper

from src.features.student.view.student_screen import (
    StudentWrapper,
)
from src.features.book.view.frames.book_dialog import BookIssueDialogWrapper

from src.features.analytics.controller import (
    AnalyticsRepositoryImpl,
)

from src.features.record.controller.record_repository import RecordRepository


def inject(
    dbClient: DatabaseService,
) -> MainAppWrapper:

    book_repo = BookRepoImpl(db=dbClient)
    student_repo = StudentRepoImpl(db=dbClient)
    analytics_repo = AnalyticsRepositoryImpl(db=dbClient)
    record_repo = RecordRepository(db=dbClient)

    book_issue_dialog_wrapper = BookIssueDialogWrapper(
        record_repo=record_repo,
        student_repo=student_repo,
    )

    book_wrapper = BookWrapper(
        book_repo=book_repo,
        book_issue_dialog_wrapper=book_issue_dialog_wrapper,
    )

    student_wrapper = StudentWrapper(
        student_repo=student_repo,
        record_repo=record_repo,
    )

    home_screen_wrapper = HomeScreenWrapper(
        wrappers=(book_wrapper, student_wrapper),
        analytics_repo=analytics_repo,
    )

    auth_screen_wrapper = AuthScreenWrapper()

    main_app_wrapper = MainAppWrapper(
        home_screen_wrapper,
        auth_screen_wrapper,
    )

    return main_app_wrapper
