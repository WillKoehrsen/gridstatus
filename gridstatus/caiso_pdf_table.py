import pypdf_table_extraction


def get_curtailment(self, date, verbose=False):
    """Return curtailment data for a given date

    Notes:
        * requires java to be installed in order to run
        * Data available from June 30, 2016 to present

    Arguments:
        date (datetime.date, str): date to return data
        verbose: print out url being fetched. Defaults to False.

    Returns:
        pandas.DataFrame: A DataFrame of curtailment data
    """
    # round to beginning of day
    date = date.normalize()

    date_str = date.strftime("%b-%d-%Y").lower()

    pdf = None
    base_url = "http://www.caiso.com/documents/wind-solar-real-time-dispatch-curtailment-report-"

    # Base url and date string format change for dates prior to May 31, 2024
    if date < pd.Timestamp("2024-05-31", tz=date.tzinfo):
        base_url = "https://www.caiso.com/documents/wind_solarreal-timedispatchcurtailmentreport"
        date_str = date.strftime("%b%d_%Y").lower()

    # handle specific case where dec 02, 2021 has wrong year in file name
    if date_str == "dec02_2021":
        date_str = "02dec_2020"

    url = f"{base_url}{date_str}.pdf"

    msg = f"Fetching URL: {url}"
    log(msg, verbose)

    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError(f"Could not find curtailment PDF for {date}")

    import tempfile

    # Save PDF content to a temporary file since camelot requires file path
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        tmp_file.write(r.content)
        tmp_path = tmp_file.name

    import pypdf_table_extraction

    try:
        # Read all tables from PDF using camelot
        tables = pypdf_table_extraction.read_pdf(
            tmp_path, pages="all", flavor="network"
        )

        # Find table with "FUEL TYPE" column
        target_table = None
        for index, table in enumerate(tables):
            if "FUEL TYPE" in table.df.iloc[1].values:
                target_table = table.df
                break

        if target_table is None:
            raise ValueError("No curtailment table found in PDF")

        # Convert camelot table to pandas DataFrame
        df = target_table.copy()

        # Set column names from second row and reset index
        df.columns = df.iloc[1]
        df = df.drop([0, 1]).reset_index(drop=True)

        # Handle continuation tables if they exist
        for table in tables[index + 1 :]:
            extra_df = table.df
            if len(extra_df.columns) == len(df.columns):
                extra_df = extra_df.drop([0, 1]).reset_index(drop=True)
                extra_df.columns = df.columns
                df = pd.concat([df, extra_df])

        rename = {
            "DATE": "Date",
            "HOU\nR": "Hour",
            "HOUR": "Hour",
            "CURT TYPE": "Curtailment Type",
            "REASON": "Curtailment Reason",
            "FUEL TYPE": "Fuel Type",
            "CURTAILED MWH": "Curtailment (MWh)",
            "CURTAILED\nMWH": "Curtailment (MWh)",
            "CURTAILED MW": "Curtailment (MW)",
            "CURTAILED\nMW": "Curtailment (MW)",
        }

        df = df.rename(columns=rename)

        # convert from hour ending to hour beginning
        df["Hour"] = df["Hour"].astype(int) - 1

        df["Time"] = df["Hour"].apply(lambda x, date=date: date + pd.Timedelta(hours=x))

        df["Interval Start"] = df["Time"]
        df["Interval End"] = df["Time"] + pd.Timedelta(hours=1)

        df = df.drop(columns=["Date", "Hour"])

        df["Fuel Type"] = df["Fuel Type"].map(
            {
                "SOLR": "Solar",
                "WIND": "Wind",
            }
        )

        df = df[
            [
                "Time",
                "Interval Start",
                "Interval End",
                "Curtailment Type",
                "Curtailment Reason",
                "Fuel Type",
                "Curtailment (MWh)",
                "Curtailment (MW)",
            ]
        ]

        return df

    finally:
        # Clean up temporary file
        os.unlink(tmp_path)
