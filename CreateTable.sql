USE [JobSpider]
GO

/****** Object:  Table [dbo].[job51]    Script Date: 2023/6/14 3:31:08 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[job51](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[keyword] [nvarchar](20) NOT NULL,
	[title] [nvarchar](50) NULL,
	[salary] [nvarchar](max) NULL,
	[area] [nvarchar](50) NULL,
	[experience] [nvarchar](50) NULL,
	[degree] [nvarchar](20) NULL,
	[company] [nvarchar](max) NULL,
	[class] [nvarchar](20) NULL,
	[scale] [nvarchar](50) NULL,
	[industry] [nvarchar](50) NULL,
 CONSTRAINT [PK_job51] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


