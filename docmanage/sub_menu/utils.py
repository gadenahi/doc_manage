from docmanage.models import Report


def get_latest_reports():
    """
    To get the latest reports
    :return: 2 latest reports
    """
    latest_reports = Report.query.order_by(Report.date_published.desc()).\
        filter_by(status='1').limit(2)
    return latest_reports
